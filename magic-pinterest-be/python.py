from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    image = await file.read()

    # ML stuff will eventually happen here

    return {
        "filename": file.filename
    }