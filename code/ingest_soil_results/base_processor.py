from pydantic import BaseModel, Field
from datetime import datetime
import glob
import os
import pdfplumber
import re
import socket
import pandas as pd
from growbuddies_config import soil_results_config, OutputType
from typing import Dict
from abc import ABC, abstractmethod


# Pydantic model for name mapping
class NameMappingModel(BaseModel):
    # Define fields based on the structure of name_mapping.json
    # Using Dict[str, str] to represent key-value pairs
    mapping: Dict[str, str] = Field(...)


class BaseProcessor(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def process_pdf(self, pdf_file: str, output_setting: OutputType) -> None:
        pass

    def _store_pdf(self, measurement_name, df, pdf_file, output_setting) -> None:
        timestamp_ns = self._extract_timestamp_from_pdf(pdf_file)
        line_protocol = self._build_influx_row(measurement_name, df, timestamp_ns)
        if output_setting == OutputType.INFLUXDB or output_setting == OutputType.BOTH:
            self._write_row(line_protocol)
        if output_setting == OutputType.MARKDOWN or output_setting == OutputType.BOTH:
            # Write the file out to the same directory as the location of pdf file.
            directory = os.path.dirname(pdf_file)
            self._write_markdown(directory, line_protocol)

    def _get_pdf_files(self, pdf_dir_or_file):
        return (
            glob.glob(pdf_dir_or_file + "/*.pdf")
            if os.path.isdir(pdf_dir_or_file)
            else [pdf_dir_or_file]
            if os.path.isfile(pdf_dir_or_file)
            else None
        )

    def _is_file_like(self, obj):
        file_methods = ["read", "write", "seek", "tell", "close"]
        return all(hasattr(obj, method) for method in file_methods)

    def _extract_timestamp_from_pdf(self, pdf_file) -> str:
        # Extract date from the PDF text
        with pdfplumber.open(pdf_file) as pdf:
            text = pdf.pages[0].extract_text()
        date_match = re.search(r"\b\d{1,2}/\d{1,2}/\d{4}\b", text)
        # If a date is found, use it; otherwise, use the current date
        if date_match:
            date_str = date_match.group(0)
            # Parse the date string into a datetime object
            date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            # Convert the datetime object into an ISO 8601 formatted string
            iso_date_str = date_obj.isoformat()

        else:
            # Return the current date in MM/DD/YYYY format
            iso_date_str = datetime.now().isoformat()
        return iso_date_str

    def _convert_to_float(self, value_list) -> list:
        float_values = []
        for item in value_list:
            # Check if item is a string and starts with '>'
            if isinstance(item, str) and item.startswith((">", "<")):
                # Remove and convert to float
                float_values.append(float(item[1:]))
            # Check if the item is an integer or a float or a string that can be converted to a float
            elif isinstance(item, (int, float)) or (
                isinstance(item, str) and item.replace(".", "", 1).isdigit()
            ):
                float_values.append(float(item))
            # If it's an empty string or any other case, you may choose to append a NaN or 0
            else:
                float_values.append(float("nan"))
        return float_values

    def _build_dataFrame(
        self, field_names: list, values: list, pdf_file: str
    ) -> pd.DataFrame:
        float_values = self._convert_to_float(values)
        return pd.DataFrame([float_values], columns=field_names)

    def _build_influx_row(
        self, measurement_name: str, df: pd.DataFrame, timestamp_ns: int
    ) -> str:
        data = df.iloc[0]
        fields = ",".join([f"{key}={value}" for key, value in data.items()])
        line_protocol = f"{measurement_name} {fields} {timestamp_ns}"
        return line_protocol

    def _write_row(self, line_protocol: str) -> None:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Default to the "SP" port, change to "M3" if "M3" is found in the string
        udp_port = (
            soil_results_config["udp_ports"]["M3"]
            if "M3" in line_protocol
            else soil_results_config["udp_ports"]["SP"]
        )
        # Send bytes
        try:
            # Send data
            sock.sendto(line_protocol.encode(), ("gus.local", udp_port))
        finally:
            sock.close()

    def _write_markdown(self, directory: str, content: str) -> None:
        # Split the content into individual test results
        # Extract the measurement name and date
        measurement_mapping = {"SP": "Saturated Paste", "M3": "Mehlich 3"}
        raw_measurement_name = content.split(" ")[0]
        measurement_name = measurement_mapping.get(
            raw_measurement_name, raw_measurement_name
        )  # Default to raw name if not found in mapping
        date = re.search(r"\d{4}-\d{2}-\d{2}", content).group()
        filename = os.path.join(directory, f"{raw_measurement_name}_{date}.md")
        # Create a Markdown table header with measurement name and date
        markdown_table = f"## {measurement_name} Measurement Results ({date})\n\n"
        markdown_table += "| Test | Result | Unit |\n"
        markdown_table += "|------|--------|------|\n"

        # Process each test result
        test_results = content.split(",")[1:-1]  # Exclude the measurement name and date
        for result in test_results:
            test, value = result.split("=")
            test = test.replace("_", " ")
            unit = ""
            if "(" in test and ")" in test:
                unit = test[test.find("(") + 1 : test.find(")")]
                test = test[: test.find("(")].strip()
            markdown_table += f"| {test} | {value} | {unit} |\n"

        # Output (or save) the markdown table
        with open(filename, "w") as file:
            file.write(markdown_table)
