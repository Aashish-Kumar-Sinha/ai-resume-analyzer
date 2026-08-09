import fitz
import os


def extract_text(file_path):
    """
    Extract text from PDF or TXT files.
    """

    extension = os.path.splitext(file_path)[1].lower()

    # PDF
    if extension == ".pdf":
        doc = fitz.open(file_path)
        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()
        return text.strip()

    # TXT
    elif extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    else:
        raise ValueError(f"Unsupported file type: {extension}")