import os
import chromadb
from sentence_transformers import SentenceTransformer

DOCS_PATH = "knowledge_base"

embedder = SentenceTransformer("all-MiniLM-L6-v2") #converts the text to vectors
# PersistentClient saves the vector index to disk so you only index your documents once
chroma_client = chromadb.PersistentClient(path = "./chroma_store")


def build_index():
    """
    Reads all the .txt files in the knowledge base and stores them as vectors in chromadb
    """
    collection = chroma_client.get_or_create_collection(name = "finrisk_kb", metadata={"hnsw:space": "cosine"})
    if collection.count() > 0:
        print(f"Already indexed {collection.count()} chunks. Skipping...")
        return collection
    print("Building index from knowledge base documents...")

    documents = []
    metadatas = []
    ids = []

    for filename in os.listdir(DOCS_PATH):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(DOCS_PATH, filename)
        with open(filepath, "r") as f:
            text = f.read()

        #splitting the sentence into smaller chunks
        chunks = chunk_text(text, chunk_size=300, overlap = 50)
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({"source": filename})
            ids.append(f"{filename}_{i}")
    
    embeddings = embedder.encode(documents).tolist() #convert the chunks into vectors
    #store everything in chromadb
    collection.add(documents = documents, embeddings=embeddings, metadatas=metadatas, ids=ids)

    print(f"indexed {len(documents)} chunks successfully")
    return collection

def chunk_text (text, chunk_size=300, overlap=50):
    """
    Splits long document into overlapping word chunks
    """

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def query_knowledge_base(query, n_results=3):
    """
    Searches the vector database for chunks that are semantically related to the query.
    """
    collection = chroma_client.get_or_create_collection(name = "finrisk_kb")
    query_embedding = embedder.encode([query]).tolist()

    results = collection.query(query_embeddings=query_embedding, n_results=n_results)
    chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    formatted = []
    for chunk, source in zip(chunks, sources):
        formatted.append(f"[Source: {source}]\n{chunk}")
    return "\n\n---\n\n".join(formatted)





