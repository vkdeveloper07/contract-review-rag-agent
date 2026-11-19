from contract_review.rag.models import Chunk


def store_chunks(chunks: list[Chunk], collection) -> int:
    if not chunks:
        return 0
    collection.add(
        ids=[chunk.id for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        metadatas=[{"source": chunk.source, "location": chunk.location} for chunk in chunks],
    )
    return collection.count()
