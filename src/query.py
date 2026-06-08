import os
import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "golden_retriever_guide"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def retrieve_chunks(question, top_k=5):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)

    query_embedding = embedding_model.encode([question]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = []

    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i]
        })

    return chunks


def build_context(chunks):
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['source']}, chunk {chunk['chunk_index']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context_parts)


def ask(question, top_k=5):
    chunks = retrieve_chunks(question, top_k=top_k)
    context = build_context(chunks)

    sources = sorted(set(chunk["source"] for chunk in chunks))

    system_prompt = """
You are a grounded question-answering assistant for a Golden Retriever guide.

You must answer using ONLY the provided context.
Do not use outside knowledge.
If the context does not contain enough information to answer, say:
"I don't have enough information in the provided sources to answer that."

Keep the answer clear and concise.
Mention the relevant source names when possible.
"""

    user_prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }


if __name__ == "__main__":
    test_questions = [
        "Are Golden Retrievers usually good family dogs?",
        "How much exercise do Golden Retrievers need?",
        "What are some challenges of owning a Golden Retriever?",
        "What is the best laptop for a college student?"
    ]

    for question in test_questions:
        print("\nQUESTION:", question)
        result = ask(question)
        print("\nANSWER:")
        print(result["answer"])
        print("\nSOURCES:")
        for source in result["sources"]:
            print("-", source)
        print("=" * 80)