from app.cleaning import clean_text


def test_removes_leading_and_trailing_whitespace():
    text = "   Torilo Academy   "

    cleaned = clean_text(text)

    assert cleaned == "Torilo Academy"


def test_collapses_multiple_spaces():
    text = "Software    Engineering     Course"

    cleaned = clean_text(text)

    assert cleaned == "Software Engineering Course"


def test_collapses_excessive_blank_lines():
    text = "Torilo Academy\n\n\n\nSoftware Engineering"

    cleaned = clean_text(text)

    assert cleaned == "Torilo Academy\n\nSoftware Engineering"


def test_preserves_meaningful_content():
    text = "Software Engineering — 12 weeks\nFee: ₦250,000"

    cleaned = clean_text(text)

    assert "Software Engineering" in cleaned
    assert "12 weeks" in cleaned
    assert "₦250,000" in cleaned
