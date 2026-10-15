from app.chunking import chunk_text, create_document_chunks
from app.documents import load_documents


def test_empty_text_returns_empty_list():
    chunks = chunk_text("")
    assert chunks == []


def test_short_text_returns_one_chunk():
    text = "Torilo Academy"
    chunks = chunk_text(text, chunk_size=800, overlap=100)

    assert len(chunks) == 1
    assert chunks[0] == text


def test_long_text_creates_multiple_chunks():
    text = "A" * 2000
    chunks = chunk_text(text, chunk_size=800, overlap=100)

    assert len(chunks) > 1


def test_chunks_do_not_exceed_chunk_size():
    text = "A" * 2000
    chunks = chunk_text(text, chunk_size=800, overlap=100)

    for chunk in chunks:
        assert len(chunk) <= 800


def test_invalid_overlap_raises_error():
    text = "Torilo Academy"

    try:
        chunk_text(text, chunk_size=100, overlap=100)
        assert False
    except ValueError:
        assert True


# ---------------------------------------------------------
# Integration tests for create_document_chunks()
# ---------------------------------------------------------

def test_all_documents_produce_chunks():
    documents = load_documents()
    chunks = create_document_chunks(documents)

    assert len(documents) == 16
    assert len(chunks) > 0


def test_every_chunk_has_required_fields():
    documents = load_documents()
    chunks = create_document_chunks(documents)

    for chunk in chunks:
        assert "source" in chunk
        assert "chunk_id" in chunk
        assert "text" in chunk


def test_chunk_sources_are_valid():
    documents = load_documents()
    chunks = create_document_chunks(documents)

    expected_sources = {
        document["source"]
        for document in documents
    }

    for chunk in chunks:
        assert chunk["source"] in expected_sources


def test_chunk_ids_are_unique():
    documents = load_documents()
    chunks = create_document_chunks(documents)

    chunk_ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    assert len(chunk_ids) == len(set(chunk_ids))


def test_chunk_text_is_not_empty():
    documents = load_documents()
    chunks = create_document_chunks(documents)

    for chunk in chunks:
        assert chunk["text"].strip() != ""

def test_chunk_numbers_are_sequential_per_document():
    documents = load_documents()
    chunks = create_document_chunks(documents)

    chunk_numbers_by_source = {}

    for chunk in chunks:
        source = chunk["source"]

        if source not in chunk_numbers_by_source:
            chunk_numbers_by_source[source] = []

        chunk_numbers_by_source[source].append(
            chunk["chunk_number"]
        )

    for numbers in chunk_numbers_by_source.values():
        assert numbers == list(range(1, len(numbers) + 1))


def test_document_type_is_correct():
    documents = load_documents()
    chunks = create_document_chunks(documents)

    for chunk in chunks:
        expected_type = chunk["source"].rsplit(".", 1)[0]

        assert chunk["document_type"] == expected_type


def test_metadata_fields_are_not_empty():
    documents = load_documents()
    chunks = create_document_chunks(documents)

    for chunk in chunks:
        assert chunk["source"].strip() != ""
        assert chunk["chunk_id"].strip() != ""
        assert chunk["document_type"].strip() != ""
        assert chunk["text"].strip() != ""
        assert isinstance(chunk["chunk_number"], int)
        assert chunk["chunk_number"] >= 1
