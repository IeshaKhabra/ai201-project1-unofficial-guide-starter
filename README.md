# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

     My project is a Golden Retriever unoffical guide. The system answers questions about Golden Retrievers temperment, excercise needs, trainability, grooming, family life, and ownership challenges. It is useful because people looking into getting goldens often need more than a short greed summary.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | American Kennel Club Golden Retriever Page| Breed Guide| akc_breed.txt|
| 2 | Reddit Dogs thread| Owner discussion| reddit.txt|
| 3 | Wagbar Golden retriever guide| Breed guide| wagbar.txt|
| 4 | Hills pet golden retriever page| Vet guide| hills.txt|
| 5 | PetMD golden retriever guide| Vet guide| pedmd.txt|
| 6 | Golden Retriever club of america| Breed club guide| golden_retriever_club_of_america.txt|
| 7 | Royal Kennel Golden Retriever page| Kennel club guide| royalKennel.txt|
| 8 | AKC fun facts about golden retrievers| breed article| akc_funfacts.txt|
| 9 | Vetericyn golden retriever guide| care article| vetericyn.txt|
| 10 | Chastain Vets Golden retriever page| Vet guide| chastainvets.txt|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 700 characters

**Overlap:** 150

**Why these choices fit your documents:**
     I chose this chunk size because most of my sources are article breed guides with short sections on temperment, excercise, grooming, health, and family life. A 700 character chunk is enough to capture a complete idea while the 150 character overlap preserves the context.

**Final chunk count:** 170

**Sample Chunks:** 
     Sample chunk 1 — vetericyn.txt
     “The Golden Retriever is the lovable goofball of the dog world... they make for great family pets...”

     Sample chunk 2 — wagbar.txt
     “Adult Golden Retrievers need at least 60-90 minutes of exercise daily, including both physical activity and mental stimulation...”

     Sample chunk 3 — reddit.txt
     “Worst traits — they’re active, so you need to ensure that you have the time to take them for walks and play with them...”

     Sample chunk 4 — golden_retriever_club_of_america.txt
     “The buyer has an equally important responsibility to carefully evaluate how well the breed’s characteristics match their family’s needs and limitations...”

     Sample chunk 5 — chastainvets.txt
     “Exercise is a must for them, and a good swim is often the best way to expend their boundless energy...”
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 from sentence-transformers

**Production tradeoff reflection:**
     I used this because it runs locally and is free. If I were doing this for production I would look for models based on retrieval accuracy, latency, and cost. 

Retrieval Results
Query 1

Question: Are Golden Retrievers usually good family dogs?

Top retrieved source: vetericyn.txt

Retrieval quality: Relevant

The top chunk directly mentioned Golden Retrievers being friendly with humans, especially children, and described them as great family pets.

Query 2

Question: How much exercise do Golden Retrievers need?

Top retrieved source: wagbar.txt

Retrieval quality: Relevant

The top chunk directly answered the question by saying adult Golden Retrievers need 60–90 minutes of daily exercise, including physical activity and mental stimulation.

Query 3

Question: What are some challenges of owning a Golden Retriever?

Top retrieved sources: reddit.txt, golden_retriever_club_of_america.txt, chastainvets.txt

Retrieval quality: Partially relevant

The retrieved chunks included useful information about energy level, exercise needs, health concerns, grooming, and cancer risk. However, the results were more scattered than the other queries and did not return one clean chunk that summarized all major challenges.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
     The system prompt tells the model to answer using only the retrieved context. It instructs the model not to use outside knowledge and to say "I dont have enough information in the provided sources to answer that" when the chunks are not enough

**How source attribution is surfaced in the response:**
     First the recieved chunks are passed to the LLM with source names. Second the app displays a seperate recieved from section using the source data stored in ChromaDB

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Are Golden Retrievers usually good family dogs?| Yes. They are generally friendly, affectionate, and good with families, but still need training and attention.| The system said yes and explained that they are friendly, gentle, loyal, and good with children.| Relevant| Accurate|
| 2 | How much exercise do Golden Retrievers need?| They need regular daily exercise, play, and mental stimulation.| The system said they need 60–90 minutes daily plus mental stimulation.| Relevant| Accurate|
| 3 | Are Golden Retrievers easy to train?| They are intelligent and eager to please, but still need consistent training.| The system said yes, Golden Retrievers are usually easy to train because of their kind temperament and eagerness to please.| Relavent| Accurate|
| 4 | What are some challenges of owning a Golden Retriever?| Common challenges include shedding, grooming, high energy, attention needs, and health issues.| The system mentioned high energy, regular exercise, not mellowing down with age, health and temperament risks, cancer risk, and grooming needs.| Partially relevant| Partially accurate|
| 5 | Are Golden Retrievers a good choice for someone who is rarely home?| Probably not ideal because they are social dogs that need companionship, exercise, and interaction.| The system said no, because Golden Retrievers do not do well kept away from people and need attention, play, exercise, and family interaction.| Relevant| Accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What are some challenges of owning a Golden Retriever?

**What the system returned:**
The system returned a partially correct answer about high energy, exercise needs, health problems, and cancer risk.

**Root cause (tied to a specific pipeline stage):**
This was mostly a retrieval issue. The relevant information was spread across several different chunks and sources. Because the chunking strategy used fixed character windows, some chunks contained only part of a section or mixed multiple topics together. The retriever found related chunks, but they did not form one complete summary of all ownership challenges.

**What you would change to fix it:**
I would improve the chunking strategy by splitting by headings and paragraphs before applying character limits. This would keep sections like “Exercise,” “Grooming,” “Health,” and “Family Life” more intact.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
One way the spec helped me was planning document which made the pipeline easier to build because I already knew the chunksize, overlap, and embedding model and retrieval approch before writing the code

**One way your implementation diverged from the spec, and why:**
I originally planned to rely on cleaned articles but I used local .txt files instead of live web scraping. 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
I gave the AI my domain, document list, chunk size, overlap, and architecture diagram.
- *What it produced:*
It helped produce an ingestion and chunking script that loaded .txt files, cleaned text, created 700-character chunks with 150-character overlap, and saved chunks to JSON.
- *What I changed or overrode:*
I inspected the chunk output myself and confirmed that the chunks were readable and included source metadata.

**Instance 2**

- *What I gave the AI:*
I gave the AI my retrieval approach and asked for help connecting sentence-transformers, ChromaDB, Groq, and Gradio.
- *What it produced:*
It helped produce retrieve.py, query.py, and app.py.
- *What I changed or overrode:*
I tested the system with my own evaluation questions and verified that the out-of-scope laptop question produced a refusal instead of a hallucinated answer.
