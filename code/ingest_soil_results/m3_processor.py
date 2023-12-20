from base_processor import BaseProcessor
# from growbuddies_config import soil_results_config

import pdfplumber



class M3Processor(BaseProcessor):
    def __init__(self) -> None:
        super().__init__()
        self._measurement_name = "M3"

    def process_pdf(self, pdf_file: str, output_setting: str) -> None:
        with pdfplumber.open(pdf_file) as pdf:
            table = pdf.pages[0].extract_table()
        # As we process the pdfs, we put field names and values into this list.
        # field_names = []
        # values = []
        # # Reset the current field name for the new logic
        # current_field_name = None
        # Iterate over each row in the data
        field_names, values = self._parse_header(table,7,2)
        all_field_names = []
        all_values = []
        all_field_names.extend(field_names)
        all_values.extend(values)
        field_names, values = self._parse_bottom(table,2,7)
        all_values.extend(values)
        all_field_names.extend(field_names)

        df = self._build_dataFrame(all_field_names, all_values, pdf_file)
        self._store_pdf("M3", df, pdf_file, output_setting)

    @property
    def measurement_name(self):
        return self._measurement_name


# sp = SPPDFProcessor("/Users/happy/Documents/KISBuddy/code/soil_samples/SP/paste_report_Logan_Labs_6_30_2022.pdf")
# sp.start()
