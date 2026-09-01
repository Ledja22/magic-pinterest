# Magic Pinterest Backend

Backend service for image analysis and visual similarity search using FastAPI + PyTorch + Pillow + torchvision + PostgreSQL/pgvector.

## Structure

```
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── routes.py
│   │   └── images.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── session.py
│   ├── ml/
│   │   ├── embeddings.py
│   │   ├── tagging.py
│   │   └── preprocessing.py
│   ├── services/
│   │   └── images.py
│   ├── schemas/
│   │   └── responses.py
│   └── migrations.py
├── tests/
├── requirements.txt
├── docker-compose.yml
└── .env.example
```

## Setup

1. Create a virtual environment and install requirements:

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

2. Start PostgreSQL with pgvector using Docker:

```
cd backend
docker compose up -d db
```

3. Configure environment variables:

- Copy `.env.example` to `.env` and adjust as needed:
```
cp backend/.env.example backend/.env
```

## Run

```
uvicorn app.main:app --reload --app-dir backend
```

This exposes:
- GET /health
- POST /images/analyze
- POST /images  (upload + persist + embed)
- POST /images/search (search by image)

## API Examples

- Create image:
```
curl -F "file=@/path/to/image.jpg" http://localhost:8000/images/
```

- Search similar:
```
curl -F "file=@/path/to/query.jpg" "http://localhost:8000/images/search?top_k=5"
```

## Tests

Run pytest from the `backend` directory to ensure imports resolve properly:

```
cd backend
pytest -q
```
