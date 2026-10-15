from app.main import ToriloAcademyChatbot


def test_course_fee_rephrased():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "What is the price of Software Engineering?"
    )

    assert result["route"] == "structured"
    assert "₦250,000" in result["answer"]


def test_course_duration_rephrased():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "How many weeks does Cloud Computing take?"
    )

    assert result["route"] == "structured"
    assert "8 weeks" in result["answer"]


def test_category_question():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "Which category does Graphic Design belong to?"
    )

    assert result["route"] == "structured"
    assert "Design and Creative" in result["answer"]


def test_policy_question():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "What does the attendance policy say?"
    )

    assert result["route"] == "knowledge"
    assert result["answer"]


def test_follow_up_question():
    chatbot = ToriloAcademyChatbot()

    first = chatbot.answer(
        "How much is Software Engineering?"
    )

    second = chatbot.answer(
        "How long is it?"
    )

    assert first["route"] == "structured"
    assert second["route"] == "structured"
    assert "12 weeks" in second["answer"]


def test_unknown_question():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "What is the weather in Lagos today?"
    )

    assert result["route"] == "unknown"
    assert result["answer"] == (
        "I do not have enough information "
        "to answer that question."
    )


def test_out_of_scope_question():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "Who is the president of Nigeria?"
    )

    assert result["route"] == "unknown"
    assert result["answer"] == (
        "I do not have enough information "
        "to answer that question."
    )


def test_irrelevant_question():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "Tell me a joke about programming."
    )

    assert result["route"] == "unknown"
    assert result["answer"] == (
        "I do not have enough information "
        "to answer that question."
    )


def test_memory_limit():
    chatbot = ToriloAcademyChatbot(
        max_memory_turns=3
    )

    chatbot.answer("How much is Software Engineering?")
    chatbot.answer("How long is it?")
    chatbot.answer("What is the attendance policy?")
    chatbot.answer("What is today's weather?")

    history = chatbot.memory.get_history()

    assert len(history) == 3