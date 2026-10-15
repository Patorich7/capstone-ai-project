import re

from app.database import get_all_courses


FOLLOW_UP_PATTERNS = [
    r"^how long is it\??$",
    r"^how long is that\??$",
    r"^how long does it last\??$",
    r"^what is its duration\??$",
    r"^what is the duration\??$",
    r"^how much is it\??$",
    r"^how much does it cost\??$",
    r"^what is its fee\??$",
    r"^what is the fee\??$",
    r"^what category is it in\??$",
    r"^which category is it in\??$",
]


def is_follow_up_question(question):
    """
    Check whether a question is a simple follow-up
    that depends on previous conversation context.
    """

    if not question or not question.strip():
        return False

    normalized = question.lower().strip()
    normalized = re.sub(r"\s+", " ", normalized)

    for pattern in FOLLOW_UP_PATTERNS:

        if re.fullmatch(pattern, normalized):
            return True

    return False


def find_course_in_history(history):
    """
    Find the most recent course mentioned in the
    conversation history.
    """

    if not history:
        return None

    courses = get_all_courses()

    programmes = [
        "Product Management",
        "AI Engineering",
    ]

    # Search recent conversation first.
    for turn in reversed(history):

        combined_text = (
            f"{turn.get('question', '')} "
            f"{turn.get('answer', '')}"
        ).lower()

        for course in courses:

            course_name = course[1]

            if course_name.lower() in combined_text:
                return course_name

        for programme in programmes:

            if programme.lower() in combined_text:
                return programme

    return None


def resolve_follow_up(question, history):
    """
    Convert a simple follow-up question into a
    complete question using recent conversation context.

    If the question is not a supported follow-up,
    return the original question.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if not is_follow_up_question(question):
        return question.strip()

    course_name = find_course_in_history(history)

    if course_name is None:
        return question.strip()

    normalized = question.lower().strip()

    if (
        "how long" in normalized
        or "duration" in normalized
    ):
        return f"How long is {course_name}?"

    if (
        "how much" in normalized
        or "cost" in normalized
        or "fee" in normalized
    ):
        return f"How much is {course_name}?"

    if "category" in normalized:
        return f"What category is {course_name} in?"

    return question.strip()


if __name__ == "__main__":

    test_history = [
        {
            "question": "How much is Software Engineering?",
            "answer": (
                "The fee for Software Engineering/Development "
                "is ₦250,000."
            ),
        }
    ]

    test_questions = [
        "How long is it?",
        "How much does it cost?",
        "What is its fee?",
        "What category is it in?",
        "What is the attendance policy?",
    ]

    print("TORILO ACADEMY CONTEXT RESOLVER TEST")
    print("=" * 60)

    print()

    print("Previous conversation:")
    print(test_history)

    print()

    for question in test_questions:

        resolved = resolve_follow_up(
            question,
            test_history
        )

        print(f"Original: {question}")
        print(f"Resolved: {resolved}")
        print("-" * 60)