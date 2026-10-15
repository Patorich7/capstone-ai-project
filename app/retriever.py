import json
from pathlib import Path

import numpy as np

from app.embeddings import EmbeddingModel


BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_STORE_FILE = BASE_DIR / "vector_store" / "embedded_chunks.json"


class Retriever:
    """
    Retrieve the most relevant knowledge-base chunks
    using cosine similarity with a small source-priority
    adjustment for course/category questions.
    """

    def __init__(self, vector_store_file=VECTOR_STORE_FILE):
        self.vector_store_file = Path(vector_store_file)

        if not self.vector_store_file.exists():
            raise FileNotFoundError(
                f"Vector store not found: {self.vector_store_file}"
            )

        with open(
            self.vector_store_file,
            "r",
            encoding="utf-8"
        ) as file:
            self.chunks = json.load(file)

        self.embedding_model = EmbeddingModel()

    @staticmethod
    def cosine_similarity(vector_a, vector_b):
        """
        Calculate cosine similarity between two vectors.
        """

        vector_a = np.asarray(vector_a)
        vector_b = np.asarray(vector_b)

        denominator = (
            np.linalg.norm(vector_a) *
            np.linalg.norm(vector_b)
        )

        if denominator == 0:
            return 0.0

        return float(
            np.dot(vector_a, vector_b) / denominator
        )

    def retrieve(self, query, top_k=3):
        """
        Retrieve the top-k most relevant chunks
        for a student question.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        query = query.strip()
        query_lower = query.lower()

        query_embedding = self.embedding_model.embed_text(query)

        results = []

        # Identify questions specifically asking about
        # courses or course categories.
        category_query = any(
            keyword in query_lower
            for keyword in [
                "what courses",
                "which courses",
                "courses available",
                "courses under",
                "courses in",
                "category",
                "categories",
            ]
        )

        for chunk in self.chunks:

            similarity = self.cosine_similarity(
                query_embedding,
                chunk["embedding"]
            )

            # Start with the actual semantic similarity.
            ranking_score = similarity

            # The course catalog is the authoritative source
            # for course/category questions.
            if (
                category_query
                and chunk["source"] == "course_catalog.txt"
            ):
                ranking_score += 0.05

            results.append(
                {
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"],
                    "chunk_number": chunk["chunk_number"],
                    "document_type": chunk["document_type"],
                    "text": chunk["text"],
                    "similarity": similarity,
                    "ranking_score": ranking_score,
                }
            )

        # Rank by the final retrieval score.
        results.sort(
            key=lambda item: item["ranking_score"],
            reverse=True
        )

        return results[:top_k]


if __name__ == "__main__":

    retriever = Retriever()

    question = "How much does Software Engineering cost?"

    results = retriever.retrieve(
        question,
        top_k=3
    )

    print("STUDENT QUESTION")
    print("=" * 70)
    print(question)
    print()

    print("TOP RETRIEVED CHUNKS")
    print("=" * 70)

    for number, result in enumerate(results, start=1):

        print(f"Result {number}")
        print(f"Source: {result['source']}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Ranking Score: {result['ranking_score']:.4f}")
        print("-" * 70)
        print(result["text"])
        print()