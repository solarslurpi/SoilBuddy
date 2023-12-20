from base_processor import BaseProcessor
from growbuddies_config import soil_results_config

import pdfplumber



class SPProcessor(BaseProcessor):
    def __init__(self) -> None:
        super().__init__()
        self._measurement_name = "SP"

    def process_pdf(self, pdf_file: str, output_setting: str) -> None:
        with pdfplumber.open(pdf_file) as pdf:
            table = pdf.pages[0].extract_table()
        field_names, values = self._parse_header(table,8,3)
        all_field_names = []
        all_values = []
        all_field_names.extend(field_names)
        all_values.extend(values)
        field_names, values = self._parse_midsection(table,8,18)
        all_field_names.extend(field_names)
        all_values.extend(values)
        field_names, values = self._parse_bottom(table,3,18)
        all_field_names.extend(field_names)
        all_values.extend(values)
        df = self._build_dataFrame(all_field_names, all_values, pdf_file)
        self._store_pdf("SP", df, pdf_file, output_setting)


    def _parse_midsection(self, table, start_row, end_row):
        values = []
        field_names = []
        for row in table[8:18]:
            # Initialize field_name, value, and unit for each row
            field_name, value, unit = None, None, None
            unit = row[2]   
            # Check if there's a new field name in the current row
            if row[1]:  # If row[1] is not empty, update the current field name
                current_field_name = row[1]
                # When no row[1], it is the meq/L measurement.
            field_name = f"{current_field_name} ({unit.strip()})" if unit else current_field_name
            # Assign the value from the fourth column, if available
            value = row[3] if row[3] else None
            if field_name and value is not None:
                mapped_field_name = soil_results_config.get("name_mapping").get(field_name, field_name)
                values.append(value)
                field_names.append(mapped_field_name)
        return field_names, values

    @property
    def measurement_name(self):
        return self._measurement_name


# sp = SPPDFProcessor("/Users/happy/Documents/KISBuddy/code/soil_samples/SP/paste_report_Logan_Labs_6_30_2022.pdf")
# sp.start()
