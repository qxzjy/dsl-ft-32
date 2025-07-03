from app.data_preprocessing import clean_data, feature_engineering

def test_clean_data(sample_data):
    cleaned_df = clean_data(sample_data)
    assert cleaned_df.isnull().sum().sum() == 0  # Ensure no NaN values
    assert cleaned_df['feature'].dtype == float  # Ensure correct data type

def test_feature_engineering(sample_data):
    engineered_df = feature_engineering(sample_data)
    assert 'feature_squared' in engineered_df.columns  # Ensure feature is added
    assert all(engineered_df['feature_squared'] == engineered_df['feature'] ** 2)
