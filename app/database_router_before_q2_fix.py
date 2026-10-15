from app.database import (
    get_course_fee,
    get_course_duration,
    get_courses_by_category,
    get_all_courses,
)


def handle_structured_question(route_result):

    if not route_result:
        raise ValueError(
            "Route result cannot be empty."
        )

    route = route_result.get("route")
    intent = route_result.get("intent")
    question = route_result.get("question", "")

    if route != "structured":
        raise ValueError(
            "handle_structured_question() only handles "
            "structured questions."
        )

    # ---------------------------------------------
    # COURSE FEE
    # ---------------------------------------------

    if intent == "course_fee":

        course_name = extract_course_name(question)

        if course_name is None:

            return {
                "success": False,
                "message": (
                    "I could not identify the course name."
                )
            }

        fee = get_course_fee(course_name)

        if fee is None:

            return {
                "success": False,
                "message": (
                    f"I could not find {course_name} "
                    "in the Torilo Academy course database."
                )
            }

        return {
            "success": True,
            "intent": "course_fee",
            "course_name": course_name,
            "fee": fee,
            "answer": (
                f"The fee for {course_name} "
                f"is ₦{fee:,.0f}."
            )
        }

    # ---------------------------------------------
    # COURSE DURATION
    # ---------------------------------------------

    if intent == "course_duration":

        course_name = extract_course_name(question)

        if course_name is None:

            return {
                "success": False,
                "message": (
                    "I could not identify the course name."
                )
            }

        duration = get_course_duration(course_name)

        if duration is None:

            return {
                "success": False,
                "message": (
                    f"I could not find {course_name} "
                    "in the Torilo Academy course database."
                )
            }

        return {
            "success": True,
            "intent": "course_duration",
            "course_name": course_name,
            "duration_weeks": duration,
            "answer": (
                f"{course_name} has a duration "
                f"of {duration} weeks."
            )
        }

    # ---------------------------------------------
    # COURSES BY CATEGORY
    # ---------------------------------------------

    if intent == "courses_by_category":

        category = extract_category(question)

        if category is None:

            return {
                "success": False,
                "message": (
                    "I could not identify the course category."
                )
            }

        courses = get_courses_by_category(category)

        if not courses:

            return {
                "success": False,
                "message": (
                    f"I could not find courses in the "
                    f"{category} category."
                )
            }

        answer_lines = [
            f"The courses in the {category} category are:"
        ]

        for course in courses:

            course_name = course[1]
            duration = course[3]
            fee = course[4]

            answer_lines.append(
                f"- {course_name} — "
                f"{duration} weeks — "
                f"₦{fee:,.0f}"
            )

        answer = "\n".join(answer_lines)

        return {
            "success": True,
            "intent": "courses_by_category",
            "category": category,
            "courses": courses,
            "answer": answer
        }

    return {
        "success": False,
        "message": (
            "The structured question type "
            "is not supported."
        )
    }


def extract_course_name(question):

    if not question or not question.strip():
        return None

    question_lower = question.lower()

    courses = get_all_courses()

    # ---------------------------------------------
    # STEP 1: Check exact official course names
    # ---------------------------------------------

    for course in courses:

        course_name = course[1]

        if course_name.lower() in question_lower:

            return course_name

    # ---------------------------------------------
    # STEP 2: Handle common shortened names
    # ---------------------------------------------

    aliases = {
        "software engineering":
            "Software Engineering/Development",

        "frontend development":
            "Frontend Web Development",

        "frontend web":
            "Frontend Web Development",

        "software testing":
            "Software Testing/Quality Assurance",

        "quality assurance":
            "Software Testing/Quality Assurance",

        "forex":
            "Forex, Stock Trading and Cryptocurrency",

        "stock trading":
            "Forex, Stock Trading and Cryptocurrency",

        "cryptocurrency":
            "Forex, Stock Trading and Cryptocurrency",

        "project management":
            "Project Management",

        "data analytics":
            "Data Analytics",

        "cloud computing":
            "Cloud Computing",

        "graphic design":
            "Graphic Design",

        "motion graphics":
            "Motion Graphics",

        "product design":
            "Product Design",

        "web design":
            "Web Design",

        "digital marketing":
            "Digital Marketing",

        "microsoft office":
            "Microsoft Office",

        "supply chain":
            "Supply Chain Management",
    }

    # Check longer aliases first.
    # This helps avoid accidental partial matches.
    sorted_aliases = sorted(
        aliases.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for alias, official_name in sorted_aliases:

        if alias in question_lower:

            return official_name

    return None


def extract_category(question):

    if not question or not question.strip():
        return None

    question_lower = question.lower()

    # ---------------------------------------------
    # STEP 1: Check whether a category is explicitly
    # mentioned in the question.
    # ---------------------------------------------

    categories = [
        "Software and Cloud",
        "Data and Business",
        "Design and Creative",
        "Digital Marketing",
    ]

    for category in categories:

        if category.lower() in question_lower:

            return category

    # ---------------------------------------------
    # STEP 2: If the question contains a course name,
    # find that course in the database and return
    # its official category.
    # ---------------------------------------------

    courses = get_all_courses()

    for course in courses:

        course_name = course[1]
        category = course[2]

        if course_name.lower() in question_lower:

            return category

    # ---------------------------------------------
    # STEP 3: Check common course aliases.
    # ---------------------------------------------

    aliases = {
        "software engineering":
            "Software Engineering/Development",

        "frontend development":
            "Frontend Web Development",

        "frontend web":
            "Frontend Web Development",

        "software testing":
            "Software Testing/Quality Assurance",

        "quality assurance":
            "Software Testing/Quality Assurance",

        "forex":
            "Forex, Stock Trading and Cryptocurrency",

        "stock trading":
            "Forex, Stock Trading and Cryptocurrency",

        "cryptocurrency":
            "Forex, Stock Trading and Cryptocurrency",

        "project management":
            "Project Management",

        "data analytics":
            "Data Analytics",

        "cloud computing":
            "Cloud Computing",

        "graphic design":
            "Graphic Design",

        "motion graphics":
            "Motion Graphics",

        "product design":
            "Product Design",

        "web design":
            "Web Design",

        "digital marketing":
            "Digital Marketing",

        "microsoft office":
            "Microsoft Office",

        "supply chain":
            "Supply Chain Management",
    }

    sorted_aliases = sorted(
        aliases.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for alias, official_name in sorted_aliases:

        if alias in question_lower:

            course = get_course_by_name(
                official_name
            )

            if course:

                return course[2]

    return None