from typing import List
from PIL import Image
from torchvision import models, transforms
import torch

_tagger_singleton = None


def get_tagger():
    global _tagger_singleton
    if _tagger_singleton is None:
        _tagger_singleton = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
        _tagger_singleton.eval()
    return _tagger_singleton


_imagenet_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def tag_image(model, image: Image.Image, top_k: int = 5) -> List[str]:
    with torch.no_grad():
        x = _imagenet_transform(image).unsqueeze(0)
        logits = model(x)
        probs = torch.nn.functional.softmax(logits, dim=1)
        values, indices = probs.topk(top_k)
        # Get class labels from weights metadata if available
        try:
            labels = models.MobileNet_V3_Small_Weights.DEFAULT.meta["categories"]
        except Exception:
            labels = None
        tags = []
        for idx in indices[0].tolist():
            if labels and idx < len(labels):
                tags.append(labels[idx])
            else:
                tags.append(f"class_{idx}")
        return tags
