from contract_review.rag.models import RetrievedChunk


def build_context(chunks: list[RetrievedChunk]) -> str:
    return "\n\n".join(
        f"[{number}] Source: {chunk.source}, {chunk.location}\n{chunk.text}"
        for number, chunk in enumerate(chunks, 1)
    )
