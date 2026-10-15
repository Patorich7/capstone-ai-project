from app.documents import load_documents


def test_document_count():
    documents = load_documents()

    assert len(documents) == 16


def test_expected_documents_exist():
    documents = load_documents()

    sources = {document["source"] for document in documents}

    expected_sources = {
        "assessment_policy.txt",
        "attendance_policy.txt",
        "course_catalog.txt",
        "faq.txt",
        "learning_procedures.txt",
        "payment_policy.txt",
        "refund_policy.txt",
        "student_conduct_policy.txt",
        "student_handbook.txt",
        "student_policy.txt",
        "support_procedures.txt",
        "academy_overview.txt",
        "ai_engineering_programme.txt",
        "enrollment_requirements.txt",
        "product_management.txt",
        "student_support.txt",
    }

    assert sources == expected_sources


def test_documents_are_not_empty():
    documents = load_documents()

    for document in documents:
        assert document["text"].strip() != ""


def test_document_structure():
    documents = load_documents()

    for document in documents:
        assert "source" in document
        assert "text" in document