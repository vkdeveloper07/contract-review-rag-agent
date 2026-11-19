from contract_review.rag.models import RetrievedChunk


def retrieve(query: str, top_k: int, collection) -> list[RetrievedChunk]:
    if collection.count() == 0:
        return []
    results = collection.query(query_texts=[query], n_results=min(top_k, collection.count()))
    return [
        RetrievedChunk(text, metadata["source"], metadata["location"], distance)
        for text, metadata, distance in zip(results["documents"][0], results["metadatas"][0], results["distances"][0])
    ]
