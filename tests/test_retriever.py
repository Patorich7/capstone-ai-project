from app.retriever import Retriever


def test_retriever_returns_results():
    retriever = Retriever()

    results = retriever.retrieve(
        "How much does Software Engineering cost?",
        top_k=1
    )

    assert len(results) == 1


def test_software_engineering_retrieval():
    retriever = Retriever()

    results = retriever.retrieve(
        "How much does Software Engineering cost?",
        top_k=1
    )

    result = results[0]

    assert result["source"] == "course_catalog.txt"
    assert "Software Engineering/Development" in result["text"]
    assert "12 weeks" in result["text"]
    assert "₦250,000" in result["text"]


def test_frontend_web_development_retrieval():
    retriever = Retriever()

    results = retriever.retrieve(
        "How long is Frontend Web Development?",
        top_k=1
    )

    result = results[0]

    assert result["source"] == "course_catalog.txt"
    assert "Frontend Web Development" in result["text"]
    assert "10 weeks" in result["text"]


def test_design_and_creative_retrieval():
    retriever = Retriever()

    results = retriever.retrieve(
        "What courses are available in Design and Creative?",
        top_k=1
    )

    result = results[0]

    assert result["source"] == "course_catalog.txt"
    assert "Product Design" in result["text"]
    assert "Graphic Design" in result["text"]
    assert "Motion Graphics" in result["text"]
    assert "Web Design" in result["text"]


def test_project_management_retrieval():
    retriever = Retriever()

    results = retriever.retrieve(
        "How much is Project Management?",
        top_k=1
    )

    result = results[0]

    assert result["source"] == "course_catalog.txt"
    assert "Project Management" in result["text"]
    assert "12 weeks" in result["text"]
    assert "₦300,000" in result["text"]


def test_cloud_computing_retrieval():
    retriever = Retriever()

    results = retriever.retrieve(
        "What is the duration of Cloud Computing?",
        top_k=1
    )

    result = results[0]

    assert result["source"] == "course_catalog.txt"
    assert "Cloud Computing" in result["text"]
    assert "8 weeks" in result["text"]


def test_graphic_design_retrieval():
    retriever = Retriever()

    results = retriever.retrieve(
        "How much does Graphic Design cost?",
        top_k=1
    )

    result = results[0]

    assert result["source"] == "course_catalog.txt"
    assert "Graphic Design" in result["text"]
    assert "8 weeks" in result["text"]
    assert "₦160,000" in result["text"]


def test_digital_marketing_retrieval():
    retriever = Retriever()

    results = retriever.retrieve(
        "What courses are available under Digital Marketing?",
        top_k=1
    )

    result = results[0]

    assert result["source"] == "course_catalog.txt"
    assert "Digital Marketing" in result["text"]
    assert "Microsoft Office" in result["text"]


def test_supply_chain_management_retrieval():
    retriever = Retriever()

    results = retriever.retrieve(
        "How much is Supply Chain Management?",
        top_k=1
    )

    result = results[0]

    assert result["source"] == "course_catalog.txt"
    assert "Supply Chain Management" in result["text"]
    assert "10 weeks" in result["text"]
    assert "₦250,000" in result["text"]


def test_top_k_returns_requested_number():
    retriever = Retriever()

    results = retriever.retrieve(
        "What courses are available?",
        top_k=3
    )

    assert len(results) == 3


def test_empty_query_raises_error():
    retriever = Retriever()

    try:
        retriever.retrieve("", top_k=1)
        assert False
    except ValueError:
        assert True


def test_invalid_top_k_raises_error():
    retriever = Retriever()

    try:
        retriever.retrieve(
            "How much is Software Engineering?",
            top_k=0
        )
        assert False
    except ValueError:
        assert True