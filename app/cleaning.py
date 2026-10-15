import re


def clean_text(text):
    """
    Clean document text without changing its substantive meaning.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Clean each line
    lines = []

    for line in text.split("\n"):
        line = line.strip()
        line = re.sub(r"[ \t]+", " ", line)
        lines.append(line)

    # Rebuild document
    text = "\n".join(lines)

    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


if __name__ == "__main__":

    sample_text = """
        Torilo Academy

        Software Engineering     —     12 weeks
        Fee: ₦250,000


    """

    cleaned = clean_text(sample_text)

    print("CLEANED TEXT")
    print("=" * 50)
    print(cleaned)
