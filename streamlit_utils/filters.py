
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


def combine_tb(df):
    tb_variants = ["TB", "TB+", "TB++","TB+Mario", "Tb+Amne"]
    df["script"] = df.apply(
        lambda row: row['script'] if row['script'] not in tb_variants else "TB",
        axis=1
    )
    return df

def get_aggregated_role_data(df):
    agg = df.groupby('role').agg(
        number_of_games=('player_result', 'size'),
        number_of_wins=('player_result', lambda x: (x == 'Win').sum())
    ).reset_index()
    agg["winrate"] = agg["number_of_wins"]/agg["number_of_games"]
    return agg