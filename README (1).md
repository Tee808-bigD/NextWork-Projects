<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# Build a RAG Document Q&A System

**Project Link:** [View Project](https://nextwork.ai/projects/00835615-1c0c-4c68-b18a-90b2192d674e)

**Author:** TAnimation TV  
**Email:** thandomzobe9@gmail.com

---

![Image](https://nextwork.ai/vibrant_lavender_shy_sheep/uploads/00835615-1c0c-4c68-b18a-90b2192d674e_w4c01czj)

## Understanding RAG and Why It Matters

### The problem RAG solves and its importance in AI engineering

In this project, I'm building a Retrieval-Augmented Generation (RAG) system that can answer questions based on private documents. This matters because it prevents AI hallucinations and allows LLMs to accurately use internal company data they were not trained on.

## Setting Up the Development Environment

### Installing dependencies and configuring the project

In this step, I'm setting up a Python virtual environment and installing the google-genai and chromadb packages so that I can isolate my project's dependencies and connect to the AI APIs safely.

### Securing the Gemini API key

I stored my key in a .env file. This is important because it prevents sensitive credentials from being hardcoded into the Python scripts, which could accidentally be exposed if the code is shared or committed to a public repository like GitHub.

![Image](https://nextwork.ai/vibrant_lavender_shy_sheep/uploads/00835615-1c0c-4c68-b18a-90b2192d674e_d7wllced)

## Exposing the LLM Knowledge Gap

### Querying Gemini directly without document context

In this step, I'm asking Gemini about a specific fact from the document (the home office stipend) so that I can see how the AI hallucinates or fails to answer because it lacks the private context, which exposes the exact problem that RAG solves.

![Image](https://nextwork.ai/vibrant_lavender_shy_sheep/uploads/00835615-1c0c-4c68-b18a-90b2192d674e_iazlmeh0)

### Why Gemini cannot answer questions about private documents

Gemini was not provided with the data.txt document. It only relies on its pre-trained public knowledge, which does not contain fictional facts about NextWork Corp.

## Chunking Documents and Building the Vector Store

### Splitting text and generating embeddings with ChromaDB

In this step, I'm setting up the document chunking function and initializing the ChromaDB vector database so that I can break the large text file into smaller pieces and prepare them to be converted into searchable embeddings.

### How overlapping chunks improve retrieval quality

Overlapping chunks means the end of one text chunk is repeated at the beginning of the next chunk. This is useful because it ensures that sentences or ideas split across chunk boundaries retain their context, preventing the Q&A system from losing meaning when a fact spans two chunks.

![Image](https://nextwork.ai/vibrant_lavender_shy_sheep/uploads/00835615-1c0c-4c68-b18a-90b2192d674e_d6xb6awn)

### Why vector embeddings enable semantic search

Computers cannot calculate the "distance" or meaning between raw words. Embeddings (vectors) place text with similar meanings close together in a mathematical space. This allows the system to do a "semantic search" to find the most relevant answer, even if the exact keywords don't match.

## Retrieving Context and Generating Grounded Answers

### Connecting retrieval and generation into a complete RAG pipeline

In this step, I'm setting up a retrieval function and a generation prompt so that I can search ChromaDB for the chunks most relevant to my question, feed those chunks into Gemini as context, and generate an accurate, grounded answer instead of a hallucination.

### Prompt engineering to prevent hallucination

The function prevents hallucination by strictly constraining the prompt. It instructs Gemini to answer using ONLY the explicitly provided context chunks, and explicitly tells it to say "I don't have enough information..." if the answer isn't there, rather than guessing from its general training data.

## Building an Interactive Q&A System with Out-of-Scope Handling

### Adding a question loop for continuous interaction

In this step, I'm adding an interactive while loop so that I can allow the user to ask multiple questions continuously without the program exiting after just one hardcoded question, and to test out-of-scope queries to ensure it doesn't hallucinate.

![Image](https://nextwork.ai/vibrant_lavender_shy_sheep/uploads/00835615-1c0c-4c68-b18a-90b2192d674e_t8jpcj1c)

### Why graceful fallback is critical for reliable AI systems

Out-of-scope handling matters because it prevents the AI from hallucinating false information. In enterprise systems, an AI confidently guessing a wrong answer (like a fake policy or incorrect medical data) is dangerous and destroys user trust. By explicitly saying "I don't know" when the retrieved context lacks the answer, the system remains reliable, honest, and safe.

## Multi-Document Support with Metadata Filtering

![Image](https://nextwork.ai/vibrant_lavender_shy_sheep/uploads/00835615-1c0c-4c68-b18a-90b2192d674e_cibh6v3u)

### How metadata filtering enables source-specific queries

In this project extension, I learned that metadata filtering changes ChromaDB's search by adding a strict where condition before the semantic search happens. Instead of searching the entire database, ChromaDB ignores any chunks that don't match the specified source file (e.g., data2.txt), ensuring the AI only receives context from the targeted document.

## Project Reflections and Key Takeaways

### Tools and concepts mastered

The key tools I used include Python, the Google Gemini API (for chat generation and text embeddings), and ChromaDB (for vector storage and semantic search). Key concepts I learnt include: text chunking and overlapping, vector embeddings, semantic retrieval, prompt engineering to prevent hallucinations (saying "I don't know"), and metadata filtering for multi-document search.

### Time investment and challenges

This project took me approximately 2 hours. The most challenging part was troubleshooting the API configurations—specifically dealing with NVIDIA's 403 permission errors and fixing the ChromaDB dimension mismatch error by implementing a custom Gemini embedding function.

I did this project today to learn how to build a RAG (Retrieval-Augmented Generation) system from scratch using Python, Google Gemini, and ChromaDB, and to understand how to prevent AI hallucinations. Another skill I want to learn is how to deploy this RAG application to a web server and integrate it with a frontend UI like React or Streamlit.

---

*Built with [NextWork](https://nextwork.ai) - [View this project](https://nextwork.ai/projects/00835615-1c0c-4c68-b18a-90b2192d674e)*
