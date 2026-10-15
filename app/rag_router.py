from app.retriever import Retriever


class RAGRouter:
    """
    Connect knowledge questions from the question router
    to the existing RAG retriever.
    """

    def __init__(self, top_k=3):
        self.top_k = top_k
        self.retriever = Retriever()

    def handle_knowledge_question(self, route_result):
        """
        Retrieve relevant knowledge-base chunks for a
        question classified as 'knowledge'.
        """

        if not route_result:
            raise ValueError("Route result cannot be empty.")

        route = route_result.get("route")
        question = route_result.get("question", "")

        if route != "knowledge":
            raise ValueError(
                "handle_knowledge_question() only handles knowledge questions."
            )

        results = self.retriever.retrieve(
            question,
            top_k=self.top_k
        )

        return {
            "success": True,
            "route": "knowledge",
            "question": question,
            "results": results
        }


if __name__ == "__main__":

    from app.router import route_question

    test_questions = [
        "What is the attendance policy?",
        "What happens if I submit an assignment late?",
        "What are the student conduct rules?",
        "How do students request academic support?",
    ]

    print("TORILO ACADEMY ROUTER → RAG TEST")
    print("=" * 70)

    rag_router = RAGRouter(top_k=3)

    for question in test_questions:

        print()
        print(f"Question: {question}")

        route_result = route_question(question)

        print(f"Route: {route_result['route']}")
        print(f"Intent: {route_result['intent']}")

        rag_result = rag_router.handle_knowledge_question(
            route_result
        )

        print()
        print("Retrieved Knowledge:")
        print("-" * 70)

        for number, result in enumerate(
            rag_result["results"],
            start=1
        ):
            print()
            print(f"Result {number}")
            print(f"Source: {result['source']}")
            print(f"Similarity: {result['similarity']:.4f}")
            print(f"Chunk ID: {result['chunk_id']}")
            print("Text:")
            print(result["text"])
            print("-" * 70)