from app.router import route_question
from app.database_router import handle_structured_question
from app.rag_router import RAGRouter
from app.llm import generate_answer
from app.memory import ConversationMemory
from app.context_resolver import resolve_follow_up


class ToriloAcademyChatbot:
    """
    Main orchestration layer for the Torilo Academy
    AI Engineering Student Assistant.

    Routes:
        structured -> SQLite
        knowledge  -> RAG -> LLM
        unknown    -> safe response

    Conversation memory:
        Stores only the most recent turns.

    Context resolution:
        Resolves simple follow-up questions locally
        before routing them.
    """

    def __init__(self, top_k=3, max_memory_turns=3):

        self.rag_router = RAGRouter(top_k=top_k)

        self.memory = ConversationMemory(
            max_turns=max_memory_turns
        )

    def answer(self, question):

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        # ---------------------------------------------
        # STEP 1: Get recent conversation history
        # ---------------------------------------------

        history = self.memory.get_history()

        # ---------------------------------------------
        # STEP 2: Resolve follow-up question
        # ---------------------------------------------

        resolved_question = resolve_follow_up(
            question,
            history
        )

        # ---------------------------------------------
        # STEP 3: Route the resolved question
        # ---------------------------------------------

        route_result = route_question(
            resolved_question
        )

        route = route_result["route"]
        intent = route_result["intent"]

        # ---------------------------------------------
        # STEP 4: Structured question -> SQLite
        # ---------------------------------------------

        if route == "structured":

            database_result = handle_structured_question(
                route_result
            )

            if database_result.get("success"):

                answer = database_result["answer"]

                self.memory.add_turn(
                    question,
                    answer
                )

                return {
                    "question": question,
                    "resolved_question": resolved_question,
                    "route": route,
                    "intent": intent,
                    "answer": answer,
                    "source": "Torilo Academy course database",
                }

            answer = database_result.get(
                "message",
                "I do not have enough information "
                "to answer that question."
            )

            self.memory.add_turn(
                question,
                answer
            )

            return {
                "question": question,
                "resolved_question": resolved_question,
                "route": route,
                "intent": intent,
                "answer": answer,
                "source": "Torilo Academy course database",
            }

        # ---------------------------------------------
        # STEP 5: Knowledge question -> RAG -> LLM
        # ---------------------------------------------

        if route == "knowledge":

            rag_result = (
                self.rag_router.handle_knowledge_question(
                    route_result
                )
            )

            retrieved_chunks = rag_result["results"]

            answer = generate_answer(
                resolved_question,
                retrieved_chunks
            )

            sources = [
                result["source"]
                for result in retrieved_chunks
            ]

            unique_sources = list(
                dict.fromkeys(sources)
            )

            self.memory.add_turn(
                question,
                answer
            )

            return {
                "question": question,
                "resolved_question": resolved_question,
                "route": route,
                "intent": intent,
                "answer": answer,
                "source": unique_sources,
                "retrieved_chunks": retrieved_chunks,
            }

        # ---------------------------------------------
        # STEP 6: Unknown question
        # ---------------------------------------------

        answer = (
            "I do not have enough information "
            "to answer that question."
        )

        self.memory.add_turn(
            question,
            answer
        )

        return {
            "question": question,
            "resolved_question": resolved_question,
            "route": route,
            "intent": intent,
            "answer": answer,
            "source": "Torilo Academy knowledge base",
        }


def print_result(result):

    print()
    print("=" * 70)
    print(
        "TORILO ACADEMY AI ENGINEERING STUDENT ASSISTANT"
    )
    print("=" * 70)

    print()
    print(
        f"Student Question: {result['question']}"
    )

    print()
    print(
        f"Resolved Question: "
        f"{result['resolved_question']}"
    )

    print()
    print(
        f"Route: {result['route']}"
    )

    print(
        f"Intent: {result['intent']}"
    )

    print()
    print("Answer:")
    print(result["answer"])

    print()
    print("Source:")

    source = result["source"]

    if isinstance(source, list):

        for item in source:
            print(f"- {item}")

    else:

        print(source)

    print("=" * 70)


if __name__ == "__main__":

    chatbot = ToriloAcademyChatbot(
        top_k=2,
        max_memory_turns=3
    )

    test_questions = [
        "How much is Software Engineering?",
        "How long is it?",
        "What is the attendance policy?",
        "What is today's weather?",
    ]

    for question in test_questions:

        result = chatbot.answer(question)

        print_result(result)

    print()
    print("=" * 70)
    print("CONVERSATION MEMORY")
    print("=" * 70)
    print()

    print(
        chatbot.memory.get_context()
    )