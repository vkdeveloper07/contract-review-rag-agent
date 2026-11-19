import chromadb


def create_session_collection(session_id: str):
    """Create an in-memory collection scoped to this Streamlit session."""
    client = chromadb.Client()
    return client.create_collection(name=f"contracts_{session_id[:24]}", metadata={"hnsw:space": "cosine"})
