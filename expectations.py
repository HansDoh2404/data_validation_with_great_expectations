import great_expectations as gx

def verify_columns_number(df) :
    return gx.expectations.ExpectTableColumnCountToEqual(
        value = df.shape[1]
    )

def verify_columns_values(df) :
    return gx.expectations.ExpectTableColumnsToMatchSet(
        column_set = list(df.columns)
    )

def verify_all_distinct_values(df, col_name) :
    return gx.expectations.ExpectColumnDistinctValuesToBeInSet(
        column=col_name,
        value_set=df[col_name].unique().tolist()
    )
