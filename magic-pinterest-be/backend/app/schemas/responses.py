from pydantic import BaseModel
from typing import List

class ImageAnalysisResponse(BaseModel):
    filename: str
    tags: List[str]
    embedding: List[float]
    similar_images: List[str]
