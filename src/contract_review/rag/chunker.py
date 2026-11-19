from contract_review.rag.models import Chunk, Page


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and overlap smaller than chunk_size")
    words, step, pieces = text.split(), chunk_size - overlap, []
    for start in range(0, len(words), step):
        piece = " ".join(words[start : start + chunk_size])
        if piece:
            pieces.append(piece)
        if start + chunk_size >= len(words):
            break
    return pieces


def chunk_pages(pages: list[Page], chunk_size: int, overlap: int) -> list[Chunk]:
    chunks = []
    for page in pages:
        for index, text in enumerate(split_text(page.text, chunk_size, overlap)):
            chunks.append(Chunk(f"{len(chunks)}", text, page.source, page.location))
    return chunks
