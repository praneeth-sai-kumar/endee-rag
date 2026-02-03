# Endee RAG – Semantic Search & Retrieval System

This project demonstrates a **practical AI/ML application** built using **Endee** as the vector database.  
It implements a **semantic search / retrieval-augmented system (RAG-style retriever)** that allows querying documents based on meaning rather than keywords.

The system ingests documents, converts them into vector embeddings using a Hugging Face model, stores them in Endee, and exposes an API to retrieve the most relevant content for a user query.

---

## 🚀 Project Overview

### Problem Statement

Traditional keyword-based search fails to capture semantic meaning. This project solves that by enabling **semantic search** over documents using vector embeddings and a high-performance vector database.

### Solution

- Convert documents into embeddings using a sentence-transformer model
- Store embeddings in **Endee Vector Database**
- Perform similarity search using cosine distance
- Expose retrieval functionality via a **FastAPI backend**

---

## 🧠 Key Features

- Semantic search over unstructured text
- Document ingestion pipeline
- Safe and repeatable ingestion (idempotent)
- REST API for querying documents
- Optional file upload ingestion endpoint
- Uses Endee as the core vector search engine

---

## 🏗️ System Architecture

Documents (.txt)
↓
Chunking
↓
Embedding Model (Hugging Face)
↓
Endee Vector Database
↓
FastAPI Backend
↓
User Query → Relevant Chunks

---

## 🧰 Technology Stack

- **Vector Database:** Endee
- **Embeddings:** sentence-transformers (Hugging Face)
- **Backend API:** FastAPI
- **Language:** Python
- **Containerization:** Docker (Endee)
- **Similarity Metric:** Cosine similarity

---

## 🗂️ Project Structure

endee-rag/
│
├── backend/
│ ├── main.py # FastAPI application
│ ├── ingest.py # Document ingestion pipeline
│ ├── rag.py # Retrieval logic
│ ├── embeddings.py # Hugging Face embedding wrapper
│ └── endee_sdk_client.py # Endee client abstraction
│
├── data/ # Documents to ingest
│
├── requirements.txt
├── README.md
└── docker-compose.yml # Endee service

---

## 📦 How Endee Is Used

Endee acts as the **core vector database** in this project.

- Stores dense vector embeddings
- Performs fast approximate nearest neighbor (ANN) search
- Supports metadata and filtering
- Enables semantic retrieval for RAG-style pipelines

Endee is accessed using:

- Python SDK
- REST API (via FastAPI backend)

---

## ⚙️ Setup & Installation

### 1️⃣ Prerequisites

- Docker & Docker Compose
- Python 3.9+
- At least 2 GB RAM
- Port `8080` and `8000` free

---

### 2️⃣ Start Endee (Vector Database)

```bash
docker compose up -d

Verify Endee is running:

http://localhost:8080

3️⃣ Install Python Dependencies
python -m pip install -r requirements.txt

4️⃣ Add Documents

Place .txt files inside the data/ directory.

Example:

data/
├── profile.txt
├── projects.txt
└── skills.txt

5️⃣ Ingest Documents
python -m backend.ingest


This will:

Generate embeddings

Create the Endee index (if not present)

Insert document vectors into Endee

6️⃣ Run the API Server
uvicorn backend.main:app --reload


API available at:

http://127.0.0.1:8000


Swagger UI:

http://127.0.0.1:8000/docs

🔍 API Usage
Query Documents

POST /query

{
  "question": "What projects has Praneeth worked on?",
  "top_k": 3
}


Response:

{
  "results": [
    {
      "score": 0.63,
      "text": "Built an AI-based recommendation system...",
      "source": "praneeth projects.txt"
    }
  ]
}

 Upload & Ingest File

POST /ingest

Upload a .txt file

File is saved and ingested automatically

📊 Notes on Similarity Scores

Similarity scores represent cosine similarity, not accuracy

Scores around 0.5 – 0.7 are normal for semantically related content

Ranking relevance is more important than absolute score

🔮 Future Improvements

Add LLM-based answer generation (full RAG)

Support PDF and DOCX ingestion

Add UI frontend

Section-aware retrieval using metadata filters

Hybrid search (dense + sparse)

🧪 Use Cases

Semantic document search

Resume / profile search

RAG pipelines

Knowledge base retrieval

AI-powered assistants

📜 License

This project is for educational and evaluation purposes.

🙌 Acknowledgements

Endee Labs for the vector database

Hugging Face for embedding models

FastAPI for backend framework
```
