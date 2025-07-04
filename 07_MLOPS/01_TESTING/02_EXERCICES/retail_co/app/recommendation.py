import torch

def recommend(model, user_id, num_users, num_items, top_n=5):
    model.eval()
    user_indices = torch.tensor([user_id] * num_items)
    item_indices = torch.arange(num_items)
    
    with torch.no_grad():
        predictions = model(user_indices, item_indices)
    
    top_items = torch.topk(predictions, top_n).indices
    return top_items.numpy()
