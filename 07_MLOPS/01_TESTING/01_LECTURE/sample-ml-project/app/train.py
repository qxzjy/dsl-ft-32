from app.data_preprocessing import load_data, clean_data, feature_engineering, split_data
from app.model import create_model, save_model, custom_loss_function

def train_model(data_file, model_file, target_column):
    # Load and preprocess the data
    df = load_data(data_file)
    df = clean_data(df)
    df = feature_engineering(df)
    
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = split_data(df, target_column)
    
    # Create and train the model
    model = create_model()
    model.train(X_train, y_train)
    
    # Evaluate the model using the custom loss function
    predictions = model.predict(X_test)
    loss = custom_loss_function(y_test, predictions)
    
    # Save the trained model
    model.save(model_file)
    
    return model, X_test, y_test, loss

if __name__ == "__main__":
    data_file = 'data/data.csv'  # Path to your dataset
    model_file = 'models/trained_model.pkl'  # Path to save your trained model
    target_column = 'target'  # Target column in your dataset

    # Train the model and evaluate it
    model, X_test, y_test, loss = train_model(data_file, model_file, target_column)
    print(f"Model trained with a custom loss of: {loss}")
