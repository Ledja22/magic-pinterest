from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.dialects.postgresql import TEXT
from pgvector.sqlalchemy import Vector
from datetime import datetime

Base = declarative_base()


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    image_path: Mapped[str] = mapped_column(TEXT, nullable=False)
    embedding: Mapped[list] = mapped_column(Vector(512))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
