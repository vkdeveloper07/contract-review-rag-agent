"""Extract text from PDF, DOCX, and TXT uploads, retaining source locations."""

from io import BytesIO

from contract_review.rag.models import Page


def load_upload(filename: str, data: bytes) -> list[Page]:
    extension = filename.lower().rsplit(".", 1)[-1]
    if extension == "pdf":
        from pypdf import PdfReader

        reader = PdfReader(BytesIO(data))
        pages = [Page(" ".join((page.extract_text() or "").split()), filename, f"page {number}") for number, page in enumerate(reader.pages, 1)]
    elif extension == "docx":
        from docx import Document

        doc = Document(BytesIO(data))
        pages = [Page(paragraph.text.strip(), filename, f"paragraph {number}") for number, paragraph in enumerate(doc.paragraphs, 1) if paragraph.text.strip()]
        for table_number, table in enumerate(doc.tables, 1):
            rows = [" | ".join(cell.text.strip() for cell in row.cells) for row in table.rows]
            if rows:
                pages.append(Page("\n".join(rows), filename, f"table {table_number}"))
    elif extension == "txt":
        pages = [Page(data.decode("utf-8-sig", errors="replace"), filename, "text file")]
    else:
        raise ValueError("Unsupported format. Choose PDF, DOCX, or TXT.")
    return [page for page in pages if page.text.strip()]
