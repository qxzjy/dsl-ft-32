import torch
from app.evaluate import evaluate_model
from app.model import RecommendationModel

def test_evaluate_model():
    test_data = torch.tensor([
        [4.0, 0.0, 3.0],
        [0.0, 5.0, 0.0],
        [1.0, 0.0, 4.0]
    ])
    model = RecommendationModel(num_users=3, num_items=3)
    mse = evaluate_model(model, test_data, num_users=3, num_items=3)
    assert mse >= 0
