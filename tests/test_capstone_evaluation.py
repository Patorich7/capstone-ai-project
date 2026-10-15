from app.main import ToriloAcademyChatbot


def test_01_course_fee_accuracy():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "How much does Software Engineering cost?"
    )

    assert result["route"] == "structured"
    assert result["intent"] == "course_fee"
    assert "₦250,000" in result["answer"]


def test_02_course_duration_accuracy():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "How many weeks is Frontend Web Development?"
    )

    assert result["route"] == "structured"
    assert result["intent"] == "course_duration"
    assert "10 weeks" in result["answer"]


def test_03_category_accuracy():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "Which category contains Graphic Design?"
    )

    assert result["route"] == "structured"
    assert result["intent"] == "courses_by_category"
    assert "Design and Creative" in result["answer"]


def test_04_rag_routing():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "What does the attendance policy say?"
    )

    assert result["route"] == "knowledge"
    assert result["intent"] == "knowledge_query"
    assert "attendance" in result["answer"].lower()


def test_05_source_attribution():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "What is the attendance policy?"
    )

    assert "attendance_policy.txt" in result["source"]


def test_06_follow_up_context():
    chatbot = ToriloAcademyChatbot()

    chatbot.answer(
        "How much is Software Engineering?"
    )

    result = chatbot.answer(
        "How long is it?"
    )

    assert result["route"] == "structured"
    assert (
        result["resolved_question"]
        == "How long is Software Engineering/Development?"
    )
    assert "12 weeks" in result["answer"]


def test_07_unknown_question_safety():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "What is the weather in Lagos today?"
    )

    assert result["route"] == "unknown"
    assert result["answer"] == (
        "I do not have enough information "
        "to answer that question."
    )


def test_08_out_of_scope_safety():
    chatbot = ToriloAcademyChatbot()

    result = chatbot.answer(
        "Who is the president of Nigeria?"
    )

    assert result["route"] == "unknown"
    assert result["answer"] == (
        "I do not have enough information "
        "to answer that question."
    )


def test_09_memory_limit():
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


def test_10_complete_conversation_flow():
    chatbot = ToriloAcademyChatbot(
        top_k=2,
        max_memory_turns=3
    )

    first = chatbot.answer(
        "How much is Software Engineering?"
    )

    second = chatbot.answer(
        "How long is it?"
    )

    third = chatbot.answer(
        "What is the attendance policy?"
    )

    fourth = chatbot.answer(
        "What is today's weather?"
    )

    assert first["route"] == "structured"
    assert "₦250,000" in first["answer"]

    assert second["route"] == "structured"
    assert "12 weeks" in second["answer"]

    assert third["route"] == "knowledge"
    assert any(
    word in third["answer"].lower()
    for word in ["attendance", "attend"]
)

    assert fourth["route"] == "unknown"
    assert fourth["answer"] == (
        "I do not have enough information "
        "to answer that question."
    )
