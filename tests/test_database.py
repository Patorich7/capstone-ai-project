from app.database import (
    get_all_courses,
    get_course_by_name,
    get_courses_by_category,
    get_course_fee,
    get_course_duration,
)


def test_total_courses():
    courses = get_all_courses()
    assert len(courses) == 14


def test_project_management():
    course = get_course_by_name("Project Management")

    assert course is not None
    assert course[1] == "Project Management"
    assert course[2] == "Data and Business"
    assert course[3] == 12
    assert course[4] == 300000


def test_graphic_design():
    course = get_course_by_name("Graphic Design")

    assert course is not None
    assert course[1] == "Graphic Design"
    assert course[2] == "Design and Creative"
    assert course[3] == 8
    assert course[4] == 160000


def test_design_and_creative_category():
    courses = get_courses_by_category("Design and Creative")

    assert len(courses) == 4

    course_names = [course[1] for course in courses]

    assert "Product Design" in course_names
    assert "Graphic Design" in course_names
    assert "Motion Graphics" in course_names
    assert "Web Design" in course_names


def test_project_management_fee():
    fee = get_course_fee("Project Management")

    assert fee == 300000


def test_cloud_computing_duration():
    duration = get_course_duration("Cloud Computing")

    assert duration == 8


def test_software_engineering_fee():
    fee = get_course_fee("Software Engineering/Development")

    assert fee == 250000


def test_frontend_web_development_duration():
    duration = get_course_duration("Frontend Web Development")

    assert duration == 10


def test_unknown_course():
    course = get_course_by_name("Unknown Course")

    assert course is None


def test_unknown_course_fee():
    fee = get_course_fee("Unknown Course")

    assert fee is None


def test_unknown_course_duration():
    duration = get_course_duration("Unknown Course")

    assert duration is None