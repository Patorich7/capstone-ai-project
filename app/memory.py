class ConversationMemory:
    """
    Small conversation memory for the Torilo Academy chatbot.

    Only a limited number of recent exchanges are retained
    to help control prompt size and token usage.
    """

    def __init__(self, max_turns=3):
        if max_turns <= 0:
            raise ValueError("max_turns must be greater than 0.")

        self.max_turns = max_turns
        self.history = []

    def add_turn(self, question, answer):
        """
        Store one student question and chatbot answer.
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty.")

        self.history.append(
            {
                "question": question.strip(),
                "answer": answer.strip(),
            }
        )

        # Keep only the most recent turns.
        self.history = self.history[-self.max_turns:]

    def get_history(self):
        """
        Return the current conversation history.
        """

        return self.history.copy()

    def clear(self):
        """
        Clear the conversation history.
        """

        self.history.clear()

    def get_context(self):
        """
        Return a compact text representation of recent history.
        """

        if not self.history:
            return ""

        context_parts = []

        for turn in self.history:

            context_parts.append(
                f"Student: {turn['question']}\n"
                f"Assistant: {turn['answer']}"
            )

        return "\n\n".join(context_parts)


if __name__ == "__main__":

    memory = ConversationMemory(max_turns=3)

    memory.add_turn(
        "How much is Software Engineering?",
        "The fee is ₦250,000."
    )

    memory.add_turn(
        "How long is it?",
        "The course has a duration of 12 weeks."
    )

    print("TORILO ACADEMY CONVERSATION MEMORY TEST")
    print("=" * 60)

    print()
    print("Stored turns:")
    print(memory.get_history())

    print()
    print("Compact conversation context:")
    print(memory.get_context())

    print()
    print("Memory test completed successfully.")