import torch
import torch.optim as optim
from app.model import RecommendationModel

def train_model(train_data, num_users, num_items, epochs=10, lr=0.01):
    model = RecommendationModel(num_users, num_items)
    optimizer = optim.SGD(model.parameters(), lr=lr)
    criterion = torch.nn.MSELoss()

    num_users_train, num_items_train = train_data.shape

    for epoch in range(epochs):
        model.train()
        total_loss = 0

        for user_idx in range(num_users_train):
            for item_idx in range(num_items_train):
                rating = train_data[user_idx, item_idx]
                if rating > 0:  # Only train on non-zero ratings
                    user = torch.tensor([user_idx], dtype=torch.long)
                    item = torch.tensor([item_idx], dtype=torch.long)
                    prediction = model(user, item)
                    
                    # Ensure prediction and rating are valid before calculating loss
                    if not torch.isnan(prediction) and not torch.isinf(prediction):
                        loss = criterion(prediction, torch.tensor([rating], dtype=torch.float32))
                        if not torch.isnan(loss) and not torch.isinf(loss):
                            optimizer.zero_grad()
                            loss.backward()
                            optimizer.step()
                            total_loss += loss.item()
        
        avg_loss = total_loss / (num_users_train * num_items_train)
        print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss}")

    return model
