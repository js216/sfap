import sys
from pathlib import Path
from docling.document_converter import DocumentConverter

def convert_pdf_to_markdown(pdf_file):
    pdf_path = Path(pdf_file)

    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found.", file=sys.stderr)
        return 1

    converter = DocumentConverter()

    try:
        result = converter.convert(pdf_path)
        content = result.document.export_to_markdown()
        # Print to standard output
        print(content)
        return 0
    except Exception as e:
        print(f"Failed to convert {pdf_path.name}: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 1_pdf_to_raw.py <file.pdf>", file=sys.stderr)
        sys.exit(1)

    pdf_file = sys.argv[1]
    sys.exit(convert_pdf_to_markdown(pdf_file))
