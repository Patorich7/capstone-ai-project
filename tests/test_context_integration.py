from app.main import ToriloAcademyChatbot


def test_direct_course_question():

    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "How much is Software Engineering?"
    )

    assert result["route"] == "structured"

    assert (
        result["answer"]
        == "The fee for Software Engineering/Development is ₦250,000."
    )


def test_follow_up_question():

    chatbot = ToriloAcademyChatbot()

    chatbot.answer(
        "How much is Software Engineering?"
    )

    result = chatbot.answer(
        "How long is it?"
    )

    assert (
        result["resolved_question"]
        == "How long is Software Engineering/Development?"
    )

    assert result["route"] == "structured"

    assert (
        result["answer"]
        == (
            "Software Engineering/Development "
            "has a duration of 12 weeks."
        )
    )


def test_knowledge_question():

    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "What is the attendance policy?"
    )

    assert result["route"] == "knowledge"

    assert result["intent"] == "knowledge_query"

    assert "attend" in result["answer"].lower()


def test_unknown_question():

    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "What is today's weather?"
    )

    assert result["route"] == "unknown"

    assert (
        result["answer"]
        == (
            "I do not have enough information "
            "to answer that question."
        )
    )


def test_multiple_follow_ups():

    chatbot = ToriloAcademyChatbot()

    first = chatbot.answer(
        "How much is Software Engineering?"
    )

    second = chatbot.answer(
        "How long is it?"
    )

    third = chatbot.answer(
        "What category is it in?"
    )

    assert first["route"] == "structured"

    assert second["route"] == "structured"

    assert third["route"] == "structured"

    assert "12 weeks" in second["answer"]

    assert "Software and Cloud" in third["answer"]


def test_memory_limit():

    chatbot = ToriloAcademyChatbot(
        max_memory_turns=3
    )

    chatbot.answer(
        "How much is Software Engineering?"
    )

    chatbot.answer(
        "How long is it?"
    )

    chatbot.answer(
        "What is the attendance policy?"
    )

    chatbot.answer(
        "What is today's weather?"
    )

    history = chatbot.memory.get_history()

    assert len(history) == 3

    assert (
        history[0]["question"]
        == "How long is it?"
    )

    assert (
        history[-1]["question"]
        == "What is today's weather?"
    )