import torch
from app.model import RecommendationModel

def test_model_initialization():
    model = RecommendationModel(num_users=10, num_items=10)
    assert isinstance(model.user_embedding, torch.nn.Embedding)
    assert isinstance(model.item_embedding, torch.nn.Embedding)

def test_forward_pass():
    model = RecommendationModel(num_users=10, num_items=10)
    user = torch.tensor([0])
    item = torch.tensor([0])
    prediction = model(user, item)
    assert prediction.shape == torch.Size([1])
