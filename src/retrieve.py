import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = Path("data/chunks.json")
CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "golden_retriever_guide"

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_vector_store():
    chunks = load_chunks()

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    documents = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"]
        }
        for chunk in chunks
    ]

    embeddings = model.encode(documents).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Added {len(chunks)} chunks to ChromaDB")


def retrieve(query, top_k=5):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    for i in range(top_k):
        print("\n" + "=" * 70)
        print(f"Result {i + 1}")
        print(f"Source: {results['metadatas'][0][i]['source']}")
        print(f"Chunk index: {results['metadatas'][0][i]['chunk_index']}")
        print(f"Distance: {results['distances'][0][i]}")
        print("-" * 70)
        print(results["documents"][0][i])


if __name__ == "__main__":
    build_vector_store()

    test_questions = [
        "Are Golden Retrievers usually good family dogs?",
        "How much exercise do Golden Retrievers need?",
        "What are some challenges of owning a Golden Retriever?"
    ]

    for question in test_questions:
        print("\n\nQUESTION:", question)
        retrieve(question, top_k=5)