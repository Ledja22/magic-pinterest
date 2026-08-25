from io import BytesIO
from PIL import Image
import torchvision.transforms as T

# Basic preprocessing: load bytes into RGB image and apply standard transforms

def load_image(raw_bytes: bytes) -> Image.Image:
    img = Image.open(BytesIO(raw_bytes)).convert("RGB")
    return img

# torchvision transforms for embedding models
_preprocess_transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def preprocess_for_model(image: Image.Image):
    tensor = _preprocess_transform(image).unsqueeze(0)
    return tensor
