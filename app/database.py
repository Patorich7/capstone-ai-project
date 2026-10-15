import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "data" / "database"
DATABASE_FILE = DATABASE_DIR / "torilo_academy.db"


COURSES = [
    {
        "course_name": "Software Engineering/Development",
        "category": "Software and Cloud",
        "duration_weeks": 12,
        "fee": 250000,
    },
    {
        "course_name": "Frontend Web Development",
        "category": "Software and Cloud",
        "duration_weeks": 10,
        "fee": 150000,
    },
    {
        "course_name": "Cloud Computing",
        "category": "Software and Cloud",
        "duration_weeks": 8,
        "fee": 180000,
    },
    {
        "course_name": "Software Testing/Quality Assurance",
        "category": "Software and Cloud",
        "duration_weeks": 8,
        "fee": 200000,
    },
    {
        "course_name": "Data Analytics",
        "category": "Data and Business",
        "duration_weeks": 10,
        "fee": 200000,
    },
    {
        "course_name": "Project Management",
        "category": "Data and Business",
        "duration_weeks": 12,
        "fee": 300000,
    },
    {
        "course_name": "Supply Chain Management",
        "category": "Data and Business",
        "duration_weeks": 10,
        "fee": 250000,
    },
    {
        "course_name": "Forex, Stock Trading and Cryptocurrency",
        "category": "Data and Business",
        "duration_weeks": 8,
        "fee": 200000,
    },
    {
        "course_name": "Product Design",
        "category": "Design and Creative",
        "duration_weeks": 8,
        "fee": 160000,
    },
    {
        "course_name": "Graphic Design",
        "category": "Design and Creative",
        "duration_weeks": 8,
        "fee": 160000,
    },
    {
        "course_name": "Motion Graphics",
        "category": "Design and Creative",
        "duration_weeks": 8,
        "fee": 160000,
    },
    {
        "course_name": "Web Design",
        "category": "Design and Creative",
        "duration_weeks": 8,
        "fee": 160000,
    },
    {
        "course_name": "Digital Marketing",
        "category": "Digital Marketing",
        "duration_weeks": 10,
        "fee": 250000,
    },
    {
        "course_name": "Microsoft Office",
        "category": "Digital Marketing",
        "duration_weeks": 8,
        "fee": 200000,
    },
]


def create_database():
    """
    Create the Torilo Academy SQLite database
    and courses table.
    """

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            duration_weeks INTEGER NOT NULL,
            fee INTEGER NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def populate_courses():
    """
    Insert the supplied Torilo Academy course
    information into the database.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    for course in COURSES:
        cursor.execute(
            """
            INSERT OR IGNORE INTO courses
            (
                course_name,
                category,
                duration_weeks,
                fee
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                course["course_name"],
                course["category"],
                course["duration_weeks"],
                course["fee"],
            ),
        )

    connection.commit()
    connection.close()


def get_all_courses():
    """
    Return all courses from the database.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            course_name,
            category,
            duration_weeks,
            fee
        FROM courses
        ORDER BY id
        """
    )

    courses = cursor.fetchall()

    connection.close()

    return courses


def get_course_by_name(course_name):
    """
    Retrieve a course using its exact course name.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            course_name,
            category,
            duration_weeks,
            fee
        FROM courses
        WHERE course_name = ?
        """,
        (course_name,)
    )

    course = cursor.fetchone()

    connection.close()

    return course


def get_courses_by_category(category):
    """
    Retrieve all courses belonging to a category.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            course_name,
            category,
            duration_weeks,
            fee
        FROM courses
        WHERE category = ?
        ORDER BY id
        """
    ,
        (category,)
    )

    courses = cursor.fetchall()

    connection.close()

    return courses


def get_course_fee(course_name):
    """
    Retrieve the fee of a specific course.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT fee
        FROM courses
        WHERE course_name = ?
        """,
        (course_name,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    return result[0]


def get_course_duration(course_name):
    """
    Retrieve the duration of a specific course.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT duration_weeks
        FROM courses
        WHERE course_name = ?
        """,
        (course_name,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    return result[0]


if __name__ == "__main__":
    create_database()
    populate_courses()

    courses = get_all_courses()

    print("Database created successfully.")
    print(f"Courses stored: {len(courses)}")
    print(f"Database file: {DATABASE_FILE}")
