from app.retriever import Retriever


def run_retrieval_tests():
    retriever = Retriever()

    questions = [
        "How much does Software Engineering cost?",
        "How long is Frontend Web Development?",
        "What courses are available in Design and Creative?",
        "How much is Project Management?",
        "What is the duration of Cloud Computing?",
        "How much does Graphic Design cost?",
        "What courses are available under Digital Marketing?",
        "How much is Supply Chain Management?",
    ]

    print("=" * 70)
    print("RETRIEVAL EVALUATION")
    print("=" * 70)

    for number, question in enumerate(questions, start=1):

        result = retriever.retrieve(
            question,
            top_k=1
        )[0]

        print()
        print(f"Test {number}")
        print("-" * 70)
        print(f"Question: {question}")
        print(f"Source: {result['source']}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Similarity: {result['similarity']:.4f}")
        print()
        print(result["text"])


if __name__ == "__main__":
    run_retrieval_tests()