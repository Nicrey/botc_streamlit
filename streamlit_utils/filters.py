

def filter_kaboom(df):
    return df[df["script"] != 'Kaboom']

def filter_teensies(df):
    return df[df["playercount"] > 6]

def filter_value_list(values, column, df):
    return df[df[column].isin(values)]

def filter_date_range(values, column, df):
    return df[(df[column] >= values[0]) & (df[column] <= values[1])]

def filter_range(values, column, df):
    return filter_date_range(values, column, df)