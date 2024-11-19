import streamlit as st

def full_data_to_player_data(df):
    """
    Transforms the full data dataset to a player view, that shows per Player:
        * Number of Games and draw Rates for each role type and team
        * Number of Wins and Winrates for each role type and team
    """
    type_list = ["townsfolk", "outsider", "minion", "demon", "good", "evil"]
    aggregations = {}

    allowed_columns = ["player","games"]
    admin_columns = ["winrate"]

    for role_type in type_list:
        if role_type == "good":
            df[f"is_{role_type}"] = df["is_townsfolk"] + df["is_outsider"]
            df[f"{role_type}_wins"] = df["townsfolk_wins"] + df["outsider_wins"]
        elif role_type == "evil":
            df[f"is_{role_type}"] = df["is_minion"] + df["is_demon"]
            df[f"{role_type}_wins"] = df["minion_wins"] + df["demon_wins"]
        else:
            df[f"is_{role_type}"] = (df["role_type"] == role_type).astype(int)
            df[f"{role_type}_wins"] = ((df["role_type"] == role_type) & (df["player_result"] == "Win")).astype(int)
        aggregations[f"{role_type}_games"] = f"is_{role_type}"
        aggregations[f"{role_type}_win"] = f"{role_type}_wins"
        allowed_columns.append(f"{role_type}_games")
        allowed_columns.append(f"{role_type}_rate")
        admin_columns.append(f"{role_type}_win_rate")

    df["wins"] = (df["player_result"] == "Win").astype(int)
    df["game_count"] = 1
    aggregations["games"] = "game_count"
    aggregations["wins"] = "wins"

    df = df.groupby("player").agg(
        **{alias: (col, "sum") for alias, col in aggregations.items()}
    ).reset_index()

    df["winrate"] = df["wins"] / df["games"] * 100
    for role_type in type_list:
        df[f"{role_type}_rate"] = df[f"{role_type}_games"] / df["games"] * 100
        df[f"{role_type}_win_rate"] = df[f"{role_type}_win"] / df[f"{role_type}_games"] * 100

    columns = allowed_columns if st.session_state.logged_in_player != 'Tim' else allowed_columns + admin_columns
    df = df[columns]
    return df