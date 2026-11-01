# RAG API

A Retrieval-Augmented Generation (RAG) API built with Django REST Framework, FAISS, and LangChain. Upload PDF or DOCX documents, then ask questions — the system retrieves relevant passages and generates answers using an LLM via OpenRouter.

---

## Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup with Docker (Recommended)](#setup-with-docker-recommended)
- [Setup Locally](#setup-locally)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)

---

## Architecture

```
documents/
  models.py       ← plain Django model, no side effects
  services.py     ← text extraction + vector store rebuild
  views.py        ← thin ViewSet, delegates to services

qa/
  models.py       ← stores question/answer history
  services.py     ← RAG chain: retriever + LLM
  views.py        ← thin views, delegates to services

config/
  vector_store.py ← FAISS index management (shared infrastructure)
  settings.py
  urls.py
```

**Stack:** Django · DRF · FAISS · LangChain · HuggingFace Embeddings (`all-MiniLM-L6-v2`) · OpenRouter LLM

---

## Prerequisites

- Docker + Docker Compose **or** Python 3.11+
- An [OpenRouter](https://openrouter.ai) API key

---

## Setup with Docker (Recommended)

```bash
# 1. Clone the repo
git clone <repo-url>
cd rag

# 2. Create your environment file
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY

# 3. Build and start
docker compose up --build
```

The API is now running at `http://localhost:8000`.

Migrations run automatically on container start. The embedding model is pre-downloaded during the Docker build step, so the first request is fast.

---

## Setup Locally

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your environment file
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY

# 4. Run migrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values.

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | Yes | API key from [openrouter.ai](https://openrouter.ai) |
| `SECRET_KEY` | Yes | Django secret key (generate a strong random string for production) |
| `DEBUG` | No | `True` for development, `False` for production (default: `True`) |
| `ALLOWED_HOSTS` | No | Comma-separated hostnames (default: `localhost,127.0.0.1`) |

---

## API Documentation

Interactive docs are available once the server is running:

| URL | Description |
|---|---|
| `http://localhost:8000/api/docs/` | Swagger UI (try endpoints directly) |
| `http://localhost:8000/api/redoc/` | ReDoc (clean reference format) |
| `http://localhost:8000/api/schema/` | Raw OpenAPI 3.0 schema (JSON) |

### Endpoints Reference

#### Documents

| Method | URL | Description |
|---|---|---|
| `GET` | `/api/documents/` | List all uploaded documents |
| `POST` | `/api/documents/` | Upload a new document (PDF or DOCX) |
| `GET` | `/api/documents/{id}/` | Retrieve a single document |
| `PUT` | `/api/documents/{id}/` | Replace a document |
| `PATCH` | `/api/documents/{id}/` | Update document fields |
| `DELETE` | `/api/documents/{id}/` | Delete a document and rebuild the index |

**Upload a document — example request:**

```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "title=Company Policy" \
  -F "file=@/path/to/document.pdf"
```

**Example response:**

```json
{
  "id": 1,
  "title": "Company Policy",
  "file": "/media/documents/document.pdf",
  "extracted_text": "...",
  "created_at": "2026-05-19T10:00:00Z",
  "updated_at": "2026-05-19T10:00:00Z"
}
```

#### Question Answering

| Method | URL | Description |
|---|---|---|
| `POST` | `/api/ask/` | Ask a question against uploaded documents |
| `GET` | `/api/history/` | List all past questions and answers |

**Ask a question — example request:**

```bash
curl -X POST http://localhost:8000/api/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the refund policy?"}'
```

**Example response:**

```json
{
  "question": "What is the refund policy?",
  "answer": "According to the documents, the refund policy allows returns within 30 days of purchase...",
  "sources": [
    {
      "document_id": 1,
      "title": "Company Policy",
      "excerpt": "Customers may request a full refund within 30 days..."
    }
  ]
}
```

---

## Running Tests

```bash
python manage.py test
```

---

## Sample Data

A sample data generator is included under `samples/`. See [samples/README.md](samples/README.md) for instructions.
