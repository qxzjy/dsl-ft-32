import pandas as pd
import great_expectations as ge

def validate_column_types(df, expected_types):
    return df.dtypes.equals(pd.Series(expected_types))

def check_for_missing_values(df):
    return df.isnull().sum().sum() == 0

def validate_data_with_ge(df):
    ge_df = ge.from_pandas(df)
    ge_df.expect_column_values_to_not_be_null('feature')
    ge_df.expect_column_values_to_be_of_type('feature', 'int')
    return ge_df.validate()
