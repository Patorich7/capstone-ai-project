import numpy as np

from app.embeddings import EmbeddingModel


def test_embedding_model_loads():
    model = EmbeddingModel()

    assert model.model is not None


def test_single_text_embedding():
    model = EmbeddingModel()

    embedding = model.embed_text(
        "Software Engineering at Torilo Academy"
    )

    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == (384,)


def test_multiple_text_embeddings():
    model = EmbeddingModel()

    texts = [
        "Software Engineering",
        "Data Analytics",
        "Cloud Computing",
    ]

    embeddings = model.embed_texts(texts)

    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape == (3, 384)


def test_empty_text_raises_error():
    model = EmbeddingModel()

    try:
        model.embed_text("")
        assert False
    except ValueError:
        assert True


def test_empty_text_list_returns_empty_list():
    model = EmbeddingModel()

    embeddings = model.embed_texts([])

    assert embeddings == []
