from app.data_preprocessing import load_data, preprocess_data, split_data
from app.train import train_model
from app.evaluate import evaluate_model
from app.recommendation import recommend

# Load and preprocess the data
data = load_data('./data/user_item_ratings.csv')
user_item_matrix = preprocess_data(data)

# Split the data into training and test sets
train_data, test_data = split_data(user_item_matrix)

# Get number of users and items
num_users, num_items = user_item_matrix.shape

# Train the model
model = train_model(train_data, num_users, num_items)

# Evaluate the model
evaluate_model(model, test_data, num_users, num_items)

# Get recommendations for a specific user
user_id = 0
recommended_items = recommend(model, user_id, num_users, num_items)
print(f"Recommended items for user {user_id}: {recommended_items}")
