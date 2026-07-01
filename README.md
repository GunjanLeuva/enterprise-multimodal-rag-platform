# enterprise-multimodal-rag-platform

```markdown
# Enterprise Multimodal RAG Platform — Backend

Backend service for the Enterprise Multimodal RAG Platform, built with **FastAPI** and **Python 3.12**.

> This module covers the **Backend Foundation** only — configuration, logging, and health checks. Authentication, database, vector store, and RAG features are introduced in later phases.

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Language | Python 3.12 |
| Config | Pydantic Settings |
| Server | Uvicorn |
| Containerization | Docker |

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # Versioned API routes
│   ├── core/            # Config, logging
│   ├── schemas/         # Pydantic schemas
│   ├── utils/           # Shared utilities
│   └── main.py          # FastAPI entrypoint
├── tests/
│   ├── unit/
│   └── integration/
├── requirements.txt
├── Dockerfile
├── .env.example
└── .gitignore
```

## Prerequisites

- Python 3.12+
- pip

## Local Setup (Windows / PowerShell)

```powershell
# Clone and enter backend folder
cd backend

# Create and activate virtual environment
python -m venv .venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env
```

## Running the Application

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API base: `http://localhost:8000`
- Interactive docs (Swagger): `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Environment Variables

See [`.env.example`](.env.example) for all required variables and defaults.

## Docker

```powershell
docker build -t rag-backend .
docker run -p 8000:8000 --env-file .env rag-backend
```

## Roadmap

- [x] Backend foundation (config, logging, health check)
- [ ] Authentication
- [ ] Workspace management
- [ ] File upload & processing
- [ ] Vector search (ChromaDB)
- [ ] RAG chat engine (Gemini)
- [ ] Streaming responses
- [ ] Frontend integration

## License

MIT
```

