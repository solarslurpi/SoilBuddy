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
        # As we process the pdfs, we put field names and values into this list.
        field_names = []
        values = []
        # Reset the current field name for the new logic
        current_field_name = None
        # Iterate over each row in the data
        for i, row in enumerate(table):
            field_name, value, unit = None, None, None

            # As of 2023, the first 8 rows of the Saturated Paste Report has
            # Col 1 = Name, Col 2 = Value. 
            if i < 8:
                field_name = row[0]
                if field_name in soil_results_config.get("readings_to_exclude"):
                    continue
                value = row[3]
            # As of 2023, the pink area is row 9 18 is the pink (anion/cation) sectopm/
            elif i >= 8 and i < 18:
                # On to the anions and cations sections (pink on the PDF table)
                if row[1]: # if no row[1], then meq/l...
                    current_field_name = row[1]  # Update the current field name
                field_name = current_field_name
                unit = row[2]
                value = (
                    row[3] if row[3] else None
                )  # Take the value from the fourth column

                field_name += f" ({unit.strip()})"
            # As of 2023, i = 18 through 21 are the $ of CA : MG: K : NA
            elif i >= 18 and i < 22:
                field_name = row[1]
                unit =  "%"
                field_name += f" ({unit.strip()})"
                value = (row[3] if row[3] else None )
            elif i >= 22: # on to the trace elements...
                field_name = row[1]
                value = (row[3] if row[3] else None )
            # If there is a field name and a value, add them to the processed data
            if field_name and value:
                # Get rid of potentical commas (,) in the values.
                value = value.replace(",", "")
                mapped_field_name = soil_results_config.get("name_mapping").get(field_name, field_name)
                values.append(value)
                field_names.append(mapped_field_name)
                    

        df = self._build_dataFrame(field_names, values, pdf_file)
        self._store_pdf("SP", df, pdf_file, output_setting)

    @property
    def measurement_name(self):
        return self._measurement_name


# sp = SPPDFProcessor("/Users/happy/Documents/KISBuddy/code/soil_samples/SP/paste_report_Logan_Labs_6_30_2022.pdf")
# sp.start()
