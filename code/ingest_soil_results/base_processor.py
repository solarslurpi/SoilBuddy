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
            self._write_obsidian_page(directory, line_protocol)

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

    def _convert_float_strs_to_float(self, value_list) -> list:
        values = []
        for item in value_list:
            # Remove commas from strings that are numbers with commas in them.
            item = item.replace(',','')
            if item.startswith((">", "<")):
                # Remove and convert to float
                values.append(float(item[1:]))
            # Check if the item is an integer or a float or a string that can be converted to a float
            elif self.is_numeric_string(item):
                values.append(float(item))
            # If it's an empty string or any other case, you may choose titemo append a NaN or 0
            else:
                values.append(item)
        return values

    def is_numeric_string(self, item):
        """
        Check if the item is an integer, a float, or a string that contains only digits and/or periods
        """
        if isinstance(item, (int, float)):
            return True
        elif isinstance(item, str):
            return all(char.isdigit() or char == '.' for char in item)
        else:
            return False 
        
    def _build_dataFrame(
        self, field_names: list, values: list, pdf_file: str
    ) -> pd.DataFrame:
        values = self._convert_float_strs_to_float(values)
        return pd.DataFrame([values], columns=field_names)

    def _build_influx_row(
        self, measurement_name: str, df: pd.DataFrame, timestamp_ns: int
    ) -> str:
        data = df.iloc[0]
        fields = ",".join([f"{key}={value}" for key, value in data.items()])
        line_protocol = f"{measurement_name} {fields} {timestamp_ns}"
        return line_protocol

    def _parse_header(self, table, nRows, value_row):
        values = []
        field_names = []

        for i, row in enumerate(table):
            # Break if the specified number of rows is reached
            if i >= nRows:
                break

            field_name = row[0].strip() if row[0] else None
            # Exclude certain fields based on configuration
            if not field_name or field_name in soil_results_config.get("readings_to_exclude", []):
                continue

            # Clean and validate value
            value = row[value_row]

            # Map field names and accumulate values if valid
            if field_name and value is not None:
                mapped_field_name = soil_results_config.get("name_mapping").get(field_name, field_name)
                values.append(value)
                field_names.append(mapped_field_name)

        return field_names, values

    def _parse_bottom(self, table, value_col, row_begin):
        values = []
        field_names = []
        for row in table[row_begin:]:
            field_name = row[1]
            value = (row[value_col] if row[value_col] else None )
            if field_name and value is not None:
                mapped_field_name = soil_results_config.get("name_mapping").get(field_name, field_name)
                values.append(value)
                field_names.append(mapped_field_name)
        return field_names, values

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

    def _write_obsidian_page(self, directory: str, content: str) -> None:
        # Split the content into individual test results
        # Extract the measurement name and date
        # measurement_mapping = {"SP": "Saturated Paste", "M3": "Mehlich 3"}
        raw_measurement_name = content.split(" ")[0]
        # measurement_name = measurement_mapping.get(
        #     raw_measurement_name, raw_measurement_name
        # )  # Default to raw name if not found in mapping
        date = re.search(r"\d{4}-\d{2}-\d{2}", content).group()
        filename = os.path.join(directory, f"{raw_measurement_name}_{date}.md")
        # Create a Markdown table header with measurement name and date
        properties = f"---\ntags: {raw_measurement_name}\n"
        properties += f"date: {date}\n"

        # Process each test result
        # Splitting the content string into parts
        # Splitting the content string into parts
        parts = content.split(',')
        # remove date from parts.
        parts[-1] = parts[-1].split(' ',1)[0]
        # Extracting and removing the date from the last part
        # date_part = parts[-1].split(' ')[-1]
        # parts[-1] = parts[-1].replace(' ' + date_part, '')

        # # Adjusting the first element to remove the measurement abbreviation (M3 or SP).
        # parts[0] = parts[0].replace(raw_measurement_name, '')
        test_results = parts
        for result in test_results:
            test, value = result.split("=")
            if raw_measurement_name in test:
                test = test.replace(raw_measurement_name + ' ', '')
            properties += f"{test} : {value} \n"
        properties += "---\n"
        # Output (or save) the markdown table
        with open(filename, "w") as file:
            file.write(properties)
