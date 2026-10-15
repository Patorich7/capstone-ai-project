import json
from pathlib import Path

from app.documents import load_documents
from app.chunking import create_document_chunks
from app.embeddings import EmbeddingModel


BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
VECTOR_STORE_FILE = VECTOR_STORE_DIR / "embedded_chunks.json"


def build_vector_store():
    """
    Create embeddings for all knowledge-base chunks
    and save them to a JSON vector store.
    """

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    documents = load_documents()

    chunks = create_document_chunks(documents)

    embedding_model = EmbeddingModel()

    embedded_chunks = embedding_model.embed_chunks(chunks)

    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            embedded_chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    return embedded_chunks


if __name__ == "__main__":
    embedded_chunks = build_vector_store()

    print("Vector store created successfully.")
    print("Documents processed successfully.")
    print(f"Chunks embedded: {len(embedded_chunks)}")
    print(f"Vector store file: {VECTOR_STORE_FILE}")
