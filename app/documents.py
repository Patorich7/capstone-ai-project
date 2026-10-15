from pathlib import Path

from app.cleaning import clean_text


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Knowledge documents directory
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"


def load_documents():
    """
    Load all TXT documents from the knowledge base
    and clean their text before returning them.
    """

    documents = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):

        try:
            raw_text = file_path.read_text(encoding="utf-8")

            cleaned_text = clean_text(raw_text)

            documents.append(
                {
                    "source": file_path.name,
                    "text": cleaned_text,
                }
            )

        except UnicodeDecodeError:
            print(f"Could not decode: {file_path.name}")

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")
    print()

    for document in documents:
        print("=" * 70)
        print(f"Source: {document['source']}")
        print("=" * 70)
        print(document["text"][:500])
        print()
