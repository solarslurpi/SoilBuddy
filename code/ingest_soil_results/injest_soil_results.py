import argparse
import glob
from pdf_processor_factory import PDFProcessorFactory
from growbuddies_config import OutputType

# Argument Parser Setup
parser = argparse.ArgumentParser(description="Soil Reports Processor")
parser.add_argument("-f", "--file", type=str, help="Path to a single PDF file")
parser.add_argument(
    "-d", "--directory", type=str, help="Path to a directory containing PDF files"
)

# Parse the arguments
args = parser.parse_args()


def process_file(file_path):
    try:
        processor = PDFProcessorFactory.get_processor(file_path)
        processor.process_pdf(file_path, OutputType.MARKDOWN)
        print(f"Successfully processed {file_path}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")


def main():
    if args.file:
        process_file(args.file)
    elif args.directory:
        pdf_files = glob.glob(args.directory + "/*.pdf")
        for pdf_file in pdf_files:
            process_file(pdf_file)
    else:
        print(
            "No file or directory path provided. Please specify a file (-f) or a directory (-d)."
        )


if __name__ == "__main__":
    main()
