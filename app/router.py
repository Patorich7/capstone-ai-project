import re


STRUCTURED_FEE_KEYWORDS = [
    "fee",
    "fees",
    "cost",
    "price",
    "how much",
    "tuition",
    "payment for",
]


STRUCTURED_DURATION_KEYWORDS = [
    "duration",
    "how long",
    "weeks",
    "length of",
    "course duration",
]


STRUCTURED_ALL_COURSES_KEYWORDS = [
    "what courses does torilo academy offer",
    "what courses does torilo offer",
    "which courses does torilo academy offer",
    "which courses does torilo offer",
    "what courses are offered by torilo academy",
    "what courses are offered by torilo",
    "courses offered by torilo academy",
    "courses offered by torilo",
    "list all courses",
    "list the courses",
]


STRUCTURED_CATEGORY_KEYWORDS = [
    "courses in",
    "courses under",
    "courses available in",
    "courses are available",
    "category",
]


ACADEMY_KNOWLEDGE_KEYWORDS = [
    "academy",
    "ai engineering",
    "artificial intelligence",
    "machine learning",
    "rag",
    "large language model",
    "large language models",
    "llm",
    "llms",
    "product management",
    "programme",
    "enrollment",
    "enrolment",
    "requirement",
    "requirements",
    "campus",
    "campuses",
    "learning format",
    "learning formats",
    "remote",
    "remotely",
    "physical",
    "physically",
    "student support",
]


ATTENDANCE_KEYWORDS = [
    "cannot attend",
    "cannot attend a class",
    "can't attend",
    "cant attend",
    "can't attend a class",
    "cant attend a class",
    "unable to attend",
    "unable to attend class",
    "miss a class",
    "missed a class",
    "missing a class",
    "cannot make it to class",
    "can't make it to class",
    "valid reason for missing",
    "reason for missing the class",
]


KNOWLEDGE_KEYWORDS = [
    "policy",
    "policies",
    "attendance",
    "assessment",
    "assignment",
    "assignments",
    "test",
    "tests",
    "exam",
    "examination",
    "late submission",
    "submit",
    "academic integrity",
    "conduct",
    "student handbook",
    "student rules",
    "refund",
    "refunds",
    "payment policy",
    "learning",
    "support",
    "academic support",
    "procedure",
    "procedures",
    "faq",
]


def normalize_question(question):
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    question = question.lower().strip()
    question = re.sub(r"\s+", " ", question)

    return question


def route_question(question):
    question = normalize_question(question)

    # Structured course fee queries.
    if any(keyword in question for keyword in STRUCTURED_FEE_KEYWORDS):
        return {
            "route": "structured",
            "intent": "course_fee",
            "question": question,
        }

    # Structured course category queries.
    if any(keyword in question for keyword in STRUCTURED_CATEGORY_KEYWORDS):
        return {
            "route": "structured",
            "intent": "courses_by_category",
            "question": question,
        }

    # Structured query for all available courses.
    if any(
        keyword in question
        for keyword in STRUCTURED_ALL_COURSES_KEYWORDS
    ):
        return {
            "route": "structured",
            "intent": "all_courses",
            "question": question,
        }

    # Academy and programme questions go to RAG.
    if any(keyword in question for keyword in ACADEMY_KNOWLEDGE_KEYWORDS):
        return {
            "route": "knowledge",
            "intent": "knowledge_query",
            "question": question,
        }

    # Attendance-specific questions go to RAG.
    if any(keyword in question for keyword in ATTENDANCE_KEYWORDS):
        return {
            "route": "knowledge",
            "intent": "knowledge_query",
            "question": question,
        }

    # Structured course duration queries.
    if any(keyword in question for keyword in STRUCTURED_DURATION_KEYWORDS):
        return {
            "route": "structured",
            "intent": "course_duration",
            "question": question,
        }

    # Existing policy/procedure knowledge queries.
    if any(keyword in question for keyword in KNOWLEDGE_KEYWORDS):
        return {
            "route": "knowledge",
            "intent": "knowledge_query",
            "question": question,
        }

    # Anything outside the approved knowledge domains remains unknown.
    return {
        "route": "unknown",
        "intent": "unknown",
        "question": question,
    }


