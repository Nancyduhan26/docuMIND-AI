import fitz


def load_pdf(pdf_file):
    """
    Reads a PDF file and returns all its text.
    """

    document = fitz.open(stream=pdf_file.read(), filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text