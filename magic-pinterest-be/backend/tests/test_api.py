import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_analyze_invalid():
    res = client.post("/images/analyze", files={"file": ("bad.txt", b"not an image", "text/plain")})
    assert res.status_code == 400


def test_analyze_image():
    # create a simple red square image in memory
    from PIL import Image
    img = Image.new("RGB", (64, 64), color=(255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    res = client.post("/images/analyze", files={"file": ("test.png", buf.getvalue(), "image/png")})
    assert res.status_code == 200
    data = res.json()
    assert data["filename"] == "test.png"
    assert isinstance(data["tags"], list)
    assert isinstance(data["embedding"], list)
    assert isinstance(data["similar_images"], list)
