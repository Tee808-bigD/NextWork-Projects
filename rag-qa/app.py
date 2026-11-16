import os
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from google import genai
from google.genai import types

# Load API key from .env
api_key = None
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY=AQ.Ab8RN6LB2QCaDNpF4ncu0RDZCa6P4tYZVBIr5kA9fhDymYAH9Q"):
                api_key = line.strip().split("=", 1)[1]

if not api_key:
    print("Error: Set your GEMINI_API_KEY in the .env file")
    exit(1)

# Initialize clients
gemini_client = genai.Client(api_key=api_key)
chroma_client = chromadb.Client()

# Custom Embedding Function for ChromaDB (prevents dimension mismatch)
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            result = gemini_client.models.embed_content(
                model="gemini-embedding-001",
                contents=text,
                config=types.EmbedContentConfig(output_dimensionality=768),
            )
            embeddings.append(result.embeddings[0].values)
        return embeddings

gemini_ef = GeminiEmbeddingFunction()

def load_and_chunk(filepath, chunk_size=500, overlap=50):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def store_chunks(collection, chunks, source_name):
    for i, chunk in enumerate(chunks):
        result = gemini_client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk,
            config=types.EmbedContentConfig(output_dimensionality=768),
        )
        embedding = result.embeddings[0].values
        collection.add(
            ids=[f"{source_name}_chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": source_name}],
        )
    print(f"Stored {len(chunks)} chunks from '{source_name}' in ChromaDB")

def retrieve(collection, question, n_results=3, source_filter=None):
    result = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=question,
        config=types.EmbedContentConfig(output_dimensionality=768),
    )
    query_embedding = result.embeddings[0].values

    query_params = {
        "query_embeddings": [query_embedding],
        "n_results": n_results,
    }

    if source_filter:
        query_params["where"] = {"source": source_filter}

    results = collection.query(**query_params)
    return results["documents"][0], results["metadatas"][0]

def generate_answer(question, context_chunks):
    context = "\n\n---\n\n".join(context_chunks)
    prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided context.
If the context does not contain enough information to answer the question, say:
"I don't have enough information in the provided documents to answer this question."

Do not make up information. Only use what is explicitly stated in the context.

Context:
{context}

Question: {question}

Answer:"""
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

def load_documents(filepaths, collection):
    """Load multiple documents and store their chunks."""
    for filepath in filepaths:
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found, skipping.")
            continue
        chunks = load_and_chunk(filepath)
        print(f"Created {len(chunks)} chunks from '{filepath}'")
        store_chunks(collection, chunks, filepath)

def main():
    # Load multiple documents
    doc_files = ["data.txt", "data2.txt"]
    collection = chroma_client.create_collection(name="documents", embedding_function=gemini_ef)

    print("Loading and processing documents...")
    load_documents(doc_files, collection)

    # Interactive question loop
    print("\n--- Multi-Document RAG Q&A System Ready ---")
    print("Ask questions about your documents. Type 'quit' to exit.")
    print("To filter by source, start with 'from:filename.txt' then your question.\n")

    while True:
        user_input = input("Your question: ").strip()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if not user_input:
            continue

        # Check for source filter
        source_filter = None
        question = user_input
        if user_input.lower().startswith("from:"):
            parts = user_input.split(" ", 1)
            if len(parts) == 2:
                source_filter = parts[0][5:]
                question = parts[1]
                print(f"(Filtering to source: {source_filter})")

        # Retrieve relevant chunks
        retrieved_chunks, metadatas = retrieve(
            collection, question, source_filter=source_filter
        )

        print("\n--- Retrieved Evidence ---")
        for i, (chunk, meta) in enumerate(zip(retrieved_chunks, metadatas)):
            print(f"[Source: {meta['source']}] {chunk[:100]}...")

        # Generate answer
        answer = generate_answer(question, retrieved_chunks)
        print(f"\n--- Answer ---\n{answer}\n")

if __name__ == "__main__":
    main()
