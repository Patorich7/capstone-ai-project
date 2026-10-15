from app.documents import load_documents


def chunk_text(text, chunk_size=800, overlap=100):
    """
    Split text into overlapping chunks while preserving
    complete words at both the beginning and end.
    """

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        target_end = min(
            start + chunk_size,
            text_length
        )

        # If this is the final chunk
        if target_end >= text_length:

            chunk = text[start:text_length].strip()

            if chunk:
                chunks.append(chunk)

            break

        # Start with the target end position
        end = target_end

        # Move backward until we find whitespace.
        # This prevents the chunk from ending
        # in the middle of a word.
        while end > start and not text[end].isspace():
            end -= 1

        # Safety fallback if no whitespace was found.
        if end == start:
            end = target_end

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Calculate the next starting position
        # while preserving the requested overlap.
        start = max(end - overlap, 0)

        # Move forward if the calculated start
        # lands in the middle of a word.
        while start < end and not text[start].isspace():
            start += 1

        # Skip whitespace before beginning the next chunk.
        while start < text_length and text[start].isspace():
            start += 1

    return chunks


def chunk_course_catalog(text):
    """
    Structure-aware chunking for the Torilo Academy
    course catalog.
    """

    if not text:
        return []

    lines = text.splitlines()

    category_names = {
        "SOFTWARE AND CLOUD",
        "DATA AND BUSINESS",
        "DESIGN AND CREATIVE",
        "DIGITAL MARKETING",
    }

    sections = []
    current_section = []

    for line in lines:

        stripped_line = line.strip()

        if stripped_line in category_names:

            if current_section:
                sections.append(
                    "\n".join(current_section).strip()
                )

            current_section = [stripped_line]

        elif current_section:
            current_section.append(line)

    if current_section:
        sections.append(
            "\n".join(current_section).strip()
        )

    return [
        section
        for section in sections
        if section
    ]


def create_document_chunks(
    documents,
    chunk_size=800,
    overlap=100
):
    """
    Create chunks from all academy documents.

    The course catalog uses structure-aware chunking.
    Other documents use word-boundary chunking.
    """

    all_chunks = []

    for document in documents:

        source = document["source"]
        text = document["text"]

        document_type = source.rsplit(".", 1)[0]

        if source == "course_catalog.txt":

            chunks = chunk_course_catalog(text)

        else:

            chunks = chunk_text(
                text,
                chunk_size=chunk_size,
                overlap=overlap
            )

        for number, chunk in enumerate(
            chunks,
            start=1
        ):

            all_chunks.append(
                {
                    "source": source,
                    "chunk_id": (
                        f"{source}_chunk_{number}"
                    ),
                    "chunk_number": number,
                    "document_type": document_type,
                    "text": chunk,
                }
            )

    return all_chunks


if __name__ == "__main__":

    documents = load_documents()

    chunks = create_document_chunks(documents)

    print(
        f"Documents loaded: {len(documents)}"
    )

    print(
        f"Total chunks created: {len(chunks)}"
    )

    print()

    for chunk in chunks[:5]:

        print("=" * 70)

        print(
            f"Source: {chunk['source']}"
        )

        print(
            f"Chunk ID: {chunk['chunk_id']}"
        )

        print(
            f"Chunk Number: {chunk['chunk_number']}"
        )

        print(
            f"Document Type: {chunk['document_type']}"
        )

        print("=" * 70)

        print(chunk["text"])

        print()