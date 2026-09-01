import os
from datetime import datetime
from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session
from pgvector.sqlalchemy import Vector

from ..db import Image
from ..ml.preprocessing import load_image
from ..ml.embeddings import get_embedding_model, embed_image


class ImageService:
    def __init__(self, storage_dir: str = "storage/images"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self._embedding_model = get_embedding_model()

    def save_upload(self, filename: str, raw_bytes: bytes) -> str:
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        safe_name = f"{ts}_{os.path.basename(filename)}"
        path = os.path.join(self.storage_dir, safe_name)
        with open(path, "wb") as f:
            f.write(raw_bytes)
        return path

    def create_image(self, db: Session, filename: str, raw_bytes: bytes) -> Image:
        # 1. Validate and load
        image = load_image(raw_bytes)
        # 2. Persist file
        image_path = self.save_upload(filename, raw_bytes)
        # 3. Embed
        embedding = embed_image(self._embedding_model, image)
        # 4. Insert DB
        db_image = Image(filename=filename, image_path=image_path, embedding=embedding)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image

    def search_similar(self, db: Session, raw_bytes: bytes, top_k: int = 10):
        image = load_image(raw_bytes)
        query_vec = embed_image(self._embedding_model, image)
        # Ensure pgvector <-> SQLAlchemy setup; using raw SQL for distance for simplicity
        # cosine_distance(a, b) = 1 - (a <#> b) with pgvector 'cosine_distance' operator "<=>" in newer versions.
        # We'll use inner product for similarity if available: ivfflat requires normalized vectors for cosine.
        stmt = text(
            """
            SELECT id, filename, 1 - (embedding <#> :qvec) AS similarity
            FROM images
            ORDER BY (embedding <#> :qvec) ASC
            LIMIT :k
            """
        )
        result = db.execute(stmt.bindparams(qvec=Vector.dim(512).bind_expression(query_vec), k=top_k))
        # Fallback if bind fails; instead, use simple parameter casting
        rows = []
        try:
            rows = list(result)
        except Exception:
            # Alternative: pass vector as Python list via casting in SQL
            result = db.execute(text(
                "SELECT id, filename, 1 - (embedding <#> :qvec) AS similarity FROM images ORDER BY (embedding <#> :qvec) ASC LIMIT :k"
            ), {"qvec": query_vec, "k": top_k})
            rows = list(result)
        return [
            {"id": r[0], "filename": r[1], "similarity": float(r[2])}
            for r in rows
        ]
