# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My domain is Golden Retriever characteristics. This knowledge is useful because people researching Golden Retrievers often need more than a breed summary, instead they want to know what the dogs are actually like to live with, energy level, grooming needs, etc. This information is spread accross breed guides, veterinary pages, kennel club resources, and owner discussions, so a RAG system can make it easier to search across sources in one place

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # |       Source      |      Description      |      URL or location       |
|---|--------------------------------------------------------------------------
| 1 |American Kennel Club | Breed Guide| https://www.akc.org/dog-breeds/golden-retriever/|
| 2 |Reddit Dogs Thread | Owner Discussion| https://www.reddit.com/r/dogs/comments/y4hdkz/best_and_worst_traits_of_golden_retrievers|
| 3 | Wagbar Golden Retriever| Breed Guide| https://www.wagbar.com/golden-retriever-complete-breed-guide-temperament-care-and-family-life|
| 4 | Hill's Pet Golden Retriever | Veterinary | https://www.hillspet.com/dog-care/dog-breeds/golden-retriever |
| 5 |PetMD Golden Retriever | Veterinary |https://www.petmd.com/dog/breeds/golden-retriever|
| 6 |Golden Retriever Club of America | Breed club Guide| https://grca.org/find-a-golden/begin-the-search/is-a-golden-retriever-right-for-you/|
| 7 | Royal Kennel Club Golden Retriever| Kennel Club breed guide| https://www.royalkennelclub.com/search/breeds-a-to-z/breeds/gundog/retriever-golden/ |
| 8 |AKC Fun Facts About Golden Retrievers | Breed Article| https://www.akc.org/expert-advice/lifestyle/fun-facts-golden-retriever/|
| 9 | Vetericyn Golden Retriever| Care Article| https://vetericyn.com/blogs/vetericyn/dog-breed-guide-the-golden-retriever?srsltid=AfmBOoro7xddv-7x8jOCjmQ_7W7WoQq7QSlYHrkjWHA7ukFlnBsnVUD_|
| 10 | Chastain Vets Golden Retriever| Veterinary| https://www.chastainvets.info/services/dogs/breeds/golden-retrievers|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 700 characters

**Overlap:** 150 characters

**Reasoning:**
     Most of my documents are breed guides or advice articles with short sections about temperment, excercise, grooming, health, and family life. A 700 character chunk should capture one complete idea of friendliness or excercise needs without combining too many unrelated topics. 150 character overlap helps preserve context when an important point continues across paragraph/section boundaries

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

     I will use semantic search with sentence transformers and ChromaDB

**Embedding model:** all-MinLM-L6-v2 because it is free and runs locally

**Top-k:** 4 or 5 chunks for each user question 

**Production tradeoff reflection:**
     If I was building this for production, I would compare embedding models based on accuracy, speed, cost and if it can run locally or needs api. But for this class local is good because it avoids costs. 

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Are Golden Retrievers usually good family dogs?| Yes, most sources describe Golden Retrievers as friendly, affectionate and good with families but they still need training excercise and attention|
| 2 | How much excercise do Golden Retrievers Need? | Golden Retrievers are active dogs that need regular daily excercise, play and mental stimulation|
| 3 | Are Golden Retrievers easy to train?| They are generally considered intelligent dogs and are eager to please which makes them trainable, but consistency and early training are still important|
| 4 | What are some challenges of owning a Golden Retrievers?| Common challenges include shedding, grooming needs, high energy, needing attention, and possible health issues|
| 5 | Are Golden Retrievers a good choice for someone who is rarely home?| Probably not ideal, because they are social dogs that need companionship, excercise, and interaction |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Some documents may contain a lot of repeated website navigation, ads, or unrelated text so cleaning up will need extra work.

2. The sources may repeat similar positive descriptions of golden retrievers but that could make it harder to retrieve details about drawbacks 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     Golden Retriever Documents 
     ↓ 
     Document Ingestion (load article text, Reddit thread text, and saved pages) 
     ↓ 
     Cleaning (remove navigation text, ads, menus, repeated headers, and empty text) 
     ↓ 
     Chunking (700-character chunks with 150-character overlap) 
     ↓ 
     Embedding (sentence-transformers: all-MiniLM-L6-v2) ↓ Vector Store (ChromaDB with source metadata) 
     ↓ 
     Retrieval (top 4–5 relevant chunks per question) 
     ↓ Grounded Generation (Groq LLM answers using only retrieved chunks) 
     ↓ 
     Answer + Source Citations
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

     -I plan to use AI tools to help implement specific parts of the pipeline
     -For document ingestion I will give the AI my documents section and ask it to help write a script that loads text from saved files and stores cleaned text with source names
     -for chunking, i will give the ai my chunking strategy section and ask it to implement chunk_text() function using 700 character chunks and 150 character overlap
     - for retrieval I will give the AI my retrieval approach and architecture sections and ask it to help connect sentence transformers with ChromaDB
     - for generation I will ask the ai to help write a grounded prompt that forces the llm to answer only from retrieved chunks and return source citations

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
