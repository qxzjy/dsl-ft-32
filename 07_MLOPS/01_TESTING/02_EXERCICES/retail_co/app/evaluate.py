import torch
from sklearn.metrics import mean_squared_error

def evaluate_model(model, test_data, num_users, num_items):
    model.eval()
    
    # We need to ensure that predictions are made only for existing user-item pairs in the test_data
    user_item_pairs = test_data.nonzero(as_tuple=False)  # Get indices of non-zero ratings
    user_indices = user_item_pairs[:, 0]  # User indices
    item_indices = user_item_pairs[:, 1]  # Item indices

    # Get the corresponding ratings
    ratings = test_data[user_indices, item_indices]

    # Generate predictions for the existing user-item pairs
    with torch.no_grad():
        predictions = model(user_indices, item_indices)
        
    # Convert tensors to numpy arrays for sklearn
    ratings = ratings.numpy()
    predictions = predictions.numpy()

    # Calculate MSE
    mse = mean_squared_error(ratings, predictions)
    print(f"Test MSE: {mse}")
    return mse


