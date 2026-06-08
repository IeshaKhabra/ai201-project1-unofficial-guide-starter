import json
import re
from pathlib import Path
from html import unescape

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")
CHUNKS_PATH = Path("data/chunks.json")

CHUNK_SIZE = 700
OVERLAP = 150


def clean_text(text):
    text = unescape(text)

    # Remove HTML tags if copied text includes any
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove common website junk phrases
    junk_patterns = [
        r"Subscribe.*",
        r"Sign up.*",
        r"Share this.*",
        r"Cookie.*",
        r"Advertisement.*",
        r"Read more.*",
        r"Skip to content.*",
        r"Privacy Policy.*",
        r"Terms of Use.*",
    ]

    for pattern in junk_patterns:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

    # Normalize spacing
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) > 100:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def process_documents():
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    all_chunks = []

    raw_files = list(RAW_DIR.glob("*.txt"))

    if not raw_files:
        raise FileNotFoundError("No .txt files found in data/raw")

    for file_path in raw_files:
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned = clean_text(raw_text)

        clean_path = CLEAN_DIR / file_path.name
        clean_path.write_text(cleaned, encoding="utf-8")

        chunks = chunk_text(cleaned)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{file_path.stem}_{i}",
                "source": file_path.name,
                "chunk_index": i,
                "text": chunk
            })

    CHUNKS_PATH.write_text(
        json.dumps(all_chunks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Processed {len(raw_files)} documents")
    print(f"Created {len(all_chunks)} chunks")
    print(f"Saved chunks to {CHUNKS_PATH}")

    print("\nSample cleaned document:")
    print("-" * 50)
    print(cleaned[:1500])

    print("\nFive sample chunks:")
    print("-" * 50)
    for chunk in all_chunks[:5]:
        print(f"\nSource: {chunk['source']}")
        print(chunk["text"][:700])
        print("-" * 50)


if __name__ == "__main__":
    process_documents()