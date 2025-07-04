import pandas as pd
from app.data_validation import validate_column_types, check_for_missing_values, validate_data_with_ge

def test_validate_column_types():
    df = pd.DataFrame({
        'feature': [1, 2, 3, 4],
        'target': [2, 4, 6, 8]
    })
    expected_types = {'feature': 'int64', 'target': 'int64'}
    assert validate_column_types(df, expected_types)

def test_check_for_missing_values():
    df = pd.DataFrame({
        'feature': [1, 2, 3, 4],
        'target': [2, 4, 6, None]
    })
    assert not check_for_missing_values(df)

def test_validate_data_with_ge():
    df = pd.DataFrame({
        'feature': [1, 2, 3, 4],
        'target': [2, 4, 6, 8]
    })
    result = validate_data_with_ge(df)
    assert result['success']