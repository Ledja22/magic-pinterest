from fastapi import APIRouter, UploadFile, File, HTTPException
from ..ml.preprocessing import load_image
from ..ml.embeddings import get_embedding_model, embed_image
from ..ml.tagging import get_tagger, tag_image
from ..schemas.responses import ImageAnalysisResponse

router = APIRouter()

# Lazy singletons initialized at import time
_embedding_model = get_embedding_model()
_tagger = get_tagger()

@router.post("/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    try:
        image = load_image(await file.read())
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Generate tags and embedding
    tags = tag_image(_tagger, image)
    embedding = embed_image(_embedding_model, image)

    return ImageAnalysisResponse(
        filename=file.filename,
        tags=tags,
        embedding=embedding,
        similar_images=[],
    )
