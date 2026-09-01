from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from ..db import get_db, Base, Image
from ..db.session import get_engine
from ..services.images import ImageService

router = APIRouter()

# Ensure tables exist at startup (simple auto-create for local dev)
engine = get_engine()
Base.metadata.create_all(bind=engine)

image_service = ImageService()

@router.post("/", summary="Upload image, persist and embed")
async def create_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    raw = await file.read()
    try:
        img = image_service.create_image(db, file.filename, raw)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")
    return {
        "id": img.id,
        "filename": img.filename,
        "image_path": img.image_path,
        "created_at": img.created_at.isoformat(),
    }


@router.post("/search", summary="Search visually similar images")
async def search_images(file: UploadFile = File(...), top_k: int = 10, db: Session = Depends(get_db)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    # Cap top_k
    if top_k is None:
        top_k = 10
    top_k = max(1, min(int(top_k), 50))
    raw = await file.read()
    try:
        results = image_service.search_similar(db, raw, top_k=top_k)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")
    return {"results": results}
