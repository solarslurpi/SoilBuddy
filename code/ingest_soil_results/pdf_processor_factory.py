import pdfplumber
from sp_processor import SPProcessor
# from m3_processor import M3Processor


class PDFProcessorFactory:
    @staticmethod
    def get_processor(pdf_file):
        def isM3Report(pdf_file: str) -> bool:
            with pdfplumber.open(pdf_file) as pdf:
                text = pdf.pages[0].extract_text()
                if "Saturated" in text:
                    return False
                return True

        isM3 = isM3Report(pdf_file)
        if not isM3:
            return SPProcessor()
        else:
            pass  # TODO: M3Processor...
