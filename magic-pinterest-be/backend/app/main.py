from fastapi import FastAPI
from .api.routes import router as api_router
from .migrations import init_db

app = FastAPI(title="Magic Pinterest Backend")

# Initialize DB at startup
@app.on_event("startup")
async def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api_router, prefix="/images")
