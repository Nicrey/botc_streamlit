

def get_aggregated_role_data(df):
    agg = df.groupby('role').agg(
        number_of_games=('player_result', 'size'),
        number_of_wins=('player_result', lambda x: (x == 'Win').sum())
    ).reset_index()
    agg["winrate"] = agg["number_of_wins"]/agg["number_of_games"]
    return agg