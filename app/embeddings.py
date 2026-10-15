from sentence_transformers import SentenceTransformer

from app.documents import load_documents
from app.chunking import create_document_chunks


EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class EmbeddingModel:
    """
    Generate semantic embeddings for text chunks.
    """

    def __init__(self, model_name=EMBEDDING_MODEL):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text):
        """
        Generate an embedding for a single text.
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        return self.model.encode(
            text,
            convert_to_numpy=True
        )

    def embed_texts(self, texts):
        """
        Generate embeddings for multiple texts.
        """
        if not texts:
            return []

        return self.model.encode(
            texts,
            convert_to_numpy=True
        )

    def embed_chunks(self, chunks):
        """
        Generate embeddings for a collection of chunks.

        The original chunk metadata is preserved and an
        embedding vector is added to each chunk.
        """

        if not chunks:
            return []

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.embed_texts(texts)

        embedded_chunks = []

        for chunk, embedding in zip(chunks, embeddings):
            embedded_chunk = chunk.copy()

            # Convert NumPy array to a normal Python list
            # so it can later be saved as JSON.
            embedded_chunk["embedding"] = embedding.tolist()

            embedded_chunks.append(embedded_chunk)

        return embedded_chunks


if __name__ == "__main__":
    documents = load_documents()

    chunks = create_document_chunks(documents)

    embedding_model = EmbeddingModel()

    embedded_chunks = embedding_model.embed_chunks(chunks)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Embedded chunks: {len(embedded_chunks)}")
    print()

    if embedded_chunks:
        first_chunk = embedded_chunks[0]

        print("First embedded chunk")
        print("=" * 70)
        print(f"Source: {first_chunk['source']}")
        print(f"Chunk ID: {first_chunk['chunk_id']}")
        print(f"Chunk Number: {first_chunk['chunk_number']}")
        print(f"Document Type: {first_chunk['document_type']}")
        print(f"Embedding dimensions: {len(first_chunk['embedding'])}")