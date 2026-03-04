import great_expectations as gx

def verify_columns_number(source_df) :
    return gx.expectations.ExpectTableColumnCountToEqual(
        value = source_df.shape[1]
    )

def verify_columns_values(source_df) :
    return gx.expectations.ExpectTableColumnsToMatchSet(
        column_set = list(source_df.columns)
    )

def verify_all_distinct_values(source_df, col_name) :
    return gx.expectations.ExpectColumnDistinctValuesToBeInSet(
        column=col_name,
        value_set=source_df[col_name].unique().tolist()
    )
