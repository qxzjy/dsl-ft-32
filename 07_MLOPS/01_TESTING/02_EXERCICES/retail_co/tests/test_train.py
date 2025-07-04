import torch
from app.train import train_model

def test_training_step():
    train_data = torch.tensor([
        [4.0, 0.0, 3.0],
        [0.0, 5.0, 0.0],
        [1.0, 0.0, 4.0]
    ])
    model = train_model(train_data, num_users=3, num_items=3, epochs=1, lr=0.01)
    assert model is not None
    # Ensure some learning has taken place (i.e., weights should not be the same as initialization)
    assert not torch.allclose(model.user_embedding.weight, torch.zeros_like(model.user_embedding.weight))
