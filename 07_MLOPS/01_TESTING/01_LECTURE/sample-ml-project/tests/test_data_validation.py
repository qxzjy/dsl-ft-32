import pandas as pd
import great_expectations as ge

def test_validate_schema(sample_data):
    expected_schema = pd.DataFrame({
        'feature': pd.Series(dtype='int64'),
        'target': pd.Series(dtype='int64')
    })

    pd.testing.assert_frame_equal(sample_data.head(0), expected_schema, check_dtype=True)


def validate_data_with_great_expectations(sample_data):
    ge_df = ge.from_pandas(sample_data)

    # Define expectations
    ge_df.expect_column_values_to_not_be_null('feature')
    ge_df.expect_column_values_to_be_in_type_list('feature', ['int64', 'float64'])
    ge_df.expect_column_values_to_be_between('feature', 1, 4)
    ge_df.expect_column_values_to_be_unique('target')

    # Validate the DataFrame and return the result
    validation_result = ge_df.validate()
    return validation_result


# Pytest function to test data validation
def test_validate_data_with_ge(sample_data):

    # Run the validation using Great Expectations
    result = validate_data_with_great_expectations(sample_data)

    # Assert that all expectations passed
    assert result["success"], f"Data validation failed: {result}"
