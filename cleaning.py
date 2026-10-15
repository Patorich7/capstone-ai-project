import re


def clean_text(text):
    """
    Clean document text without changing its substantive meaning.

    Cleaning operations:
    1. Normalize line endings.
    2. Remove leading and trailing whitespace from lines.
    3. Collapse repeated spaces.
    4. Collapse excessive blank lines.
    5. Remove leading/trailing whitespace from the complete document.
    """

    # Normalize Windows and old-style line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Clean each line
    lines = []

    for line in text.split("\n"):
        # Remove leading and trailing whitespace
        line = line.strip()

        # Collapse multiple spaces/tabs into one space
        line = re.sub(r"[ \t]+", " ", line)

        lines.append(line)

    # Rebuild the document
    text = "\n".join(lines)

    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove whitespace at the beginning and end
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