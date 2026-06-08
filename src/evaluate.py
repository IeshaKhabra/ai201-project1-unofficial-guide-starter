from query import ask

questions = [
    "Are Golden Retrievers usually good family dogs?",
    "How much exercise do Golden Retrievers need?",
    "Are Golden Retrievers easy to train?",
    "What are some challenges of owning a Golden Retriever?",
    "Are Golden Retrievers a good choice for someone who is rarely home?",
]

for i, question in enumerate(questions, start=1):
    print("\n" + "=" * 80)
    print(f"QUESTION {i}: {question}")

    result = ask(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")
    for source in result["sources"]:
        print("-", source)

    print("\nRETRIEVED CHUNKS:")
    for chunk in result["chunks"]:
        print(f"- {chunk['source']} | chunk {chunk['chunk_index']} | distance {chunk['distance']}")