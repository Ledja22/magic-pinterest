# Magic Pinterest Backend

Backend service for image analysis using FastAPI + PyTorch + Pillow + torchvision.

## Structure

```
backend/
├── app/
│   ├── main.py
│   ├── api/
│   ├── ml/
│   │   ├── embeddings.py
│   │   ├── tagging.py
│   │   └── preprocessing.py
│   ├── services/
│   └── schemas/
├── tests/
├── requirements.txt
└── README.md
```

## Setup

1. Create a virtual environment and install requirements:

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

## Run

```
uvicorn app.main:app --reload --app-dir backend
```

This exposes:
- GET /health
- POST /images/analyze

## Tests

Run pytest from the `backend` directory to ensure imports resolve properly:

```
cd backend
pytest -q
```
