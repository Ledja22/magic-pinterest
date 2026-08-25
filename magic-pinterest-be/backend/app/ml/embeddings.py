import torch
from torchvision import models
from .preprocessing import preprocess_for_model

_embedding_model_singleton = None

def get_embedding_model():
    global _embedding_model_singleton
    if _embedding_model_singleton is None:
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        # remove final classification layer to get embeddings
        model = torch.nn.Sequential(*(list(model.children())[:-1]))
        model.eval()
        _embedding_model_singleton = model
    return _embedding_model_singleton


def embed_image(model, image):
    with torch.no_grad():
        x = preprocess_for_model(image)
        feat = model(x).squeeze().flatten()
        return feat.cpu().numpy().tolist()
