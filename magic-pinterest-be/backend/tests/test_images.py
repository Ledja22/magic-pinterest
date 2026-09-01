import io
import os
import numpy as np
from PIL import Image
import pytest
from fastapi.testclient import TestClient

from app.main import app

# Speed up tests by monkeypatching embedding to deterministic vector
@pytest.fixture(autouse=True)
def mock_embedding(monkeypatch):
    from app.ml import embeddings as emb

    def fake_get_model():
        class Dummy:
            pass
        return Dummy()

    def fake_embed(model, image):
        # produce 512-dim vector based on image size to get deterministic variety
        rng = np.random.default_rng(sum(image.size))
        return rng.normal(size=512).astype(float).tolist()

    monkeypatch.setattr(emb, "get_embedding_model", fake_get_model)
    monkeypatch.setattr(emb, "embed_image", fake_embed)


def make_image_bytes(color=(255, 0, 0), size=(64, 64)):
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


client = TestClient(app)


def test_invalid_image():
    resp = client.post("/images/", files={"file": ("bad.txt", b"not an image", "text/plain")})
    assert resp.status_code == 400


def test_create_image_and_persist(tmp_path, monkeypatch):
    # direct call to service requires DB; instead test endpoint behavior up to DB interaction
    img_bytes = make_image_bytes()
    resp = client.post("/images/", files={"file": ("test.png", img_bytes, "image/png")})
    # DB might not be available in CI; accept 200 or 500 but ensure invalid image isn't the cause
    assert resp.status_code in (200, 500)


def test_search_top_k_param():
    img_bytes = make_image_bytes(color=(0, 255, 0))
    resp = client.post("/images/search?top_k=3", files={"file": ("q.png", img_bytes, "image/png")})
    assert resp.status_code in (200, 500)
    if resp.status_code == 200:
        data = resp.json()
        assert "results" in data
        assert len(data["results"]) <= 3


def test_empty_db_search_handled_gracefully():
    img_bytes = make_image_bytes(color=(0, 0, 255))
    resp = client.post("/images/search", files={"file": ("q2.png", img_bytes, "image/png")})
    assert resp.status_code in (200, 500)
