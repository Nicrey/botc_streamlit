import streamlit as st

if not st.session_state.logged_in_player:
    st.warning("Bitte einloggen :)")
    st.stop()

st.subheader("Spieler*innenübersicht")
min_games = st.select_slider("Minimum Spiele", range(50), value=10)
full_data = st.session_state.full_data
df = full_data 
df["is_town"] =(df["role_type"] == "townsfolk").astype(int)
df["is_outsider"] =(df["role_type"] == "outsider").astype(int)
df["is_minion"] =(df["role_type"] == "minion").astype(int)
df["is_demon"] =(df["role_type"] == "demon").astype(int)
df["is_good"] = df["is_town"] + df["is_outsider"]
df["is_evil"] = df["is_minion"] + df["is_demon"]

df["town_win"] = ((df["role_type"] == "townsfolk") & (df["player_result"] == "Win")).astype(int)
df["outsider_win"] = ((df["role_type"] == "outsider") & (df["player_result"] == "Win")).astype(int)
df["minion_win"] = ((df["role_type"] == "minion") & (df["player_result"] == "Win")).astype(int)
df["demon_win"] = ((df["role_type"] == "demon") & (df["player_result"] == "Win")).astype(int)
df["good_win"] = df["town_win"] + df["outsider_win"]
df["evil_win"] = df["minion_win"] + df["demon_win"]

df["wins"] = (df["player_result"] == "Win").astype(int)
df["game_count"] = 1

df = df.groupby("player").agg(
    games = ('game_count', 'sum'),
    town_games = ("is_town", 'sum'),
    outsider_games = ("is_outsider", 'sum'),
    minion_games = ("is_minion", 'sum'),
    demon_games = ("is_demon", 'sum'),
    good_games = ("is_good", 'sum'),
    evil_games = ("is_evil", 'sum'),
    town_win = ("town_win", "sum"),
    outsider_win = ("outsider_win", "sum"),
    minion_win = ("minion_win", "sum"),
    demon_win = ("demon_win", "sum"),
    good_win = ("good_win", "sum"),
    evil_win = ("evil_win", "sum"),
    wins = ("wins", "sum")
).reset_index()

df["winrate"] = df["wins"] / df["games"] * 100
df["town_rate"] = df["town_games"] / df["games"] * 100
df["outsider_rate"] = df["outsider_games"] / df["games"] * 100
df["minion_rate"] = df["minion_games"] / df["games"] * 100
df["demon_rate"] = df["demon_games"] / df["games"] * 100
df["good_rate"] = df["good_games"] / df["games"] * 100
df["evil_rate"] = df["evil_games"] / df["games"] * 100
df["town_win_rate"] = df["town_win"] / df["town_games"] * 100
df["outsider_win_rate"] = df["outsider_win"] / df["outsider_games"] * 100
df["minion_win_rate"] = df["minion_win"] / df["minion_games"] * 100
df["demon_win_rate"] = df["demon_win"] / df["demon_games"] * 100
df["good_win_rate"] = df["good_win"] / df["good_games"] * 100
df["evil_win_rate"] = df["evil_win"] / df["evil_games"] * 100


allowed_columns = [
    "player",
    "games", 
    "town_games", 
    "outsider_games", 
    "minion_games", 
    "demon_games", 
    "town_rate", 
    "outsider_rate",
    "minion_rate", 
    "demon_rate",
    "good_rate", 
    "evil_rate", 
]
admin_columns = [
    "winrate",
    "town_win_rate",
    "outsider_win_rate",
    "minion_win_rate",
    "demon_win_rate",
    "good_win_rate",
    "evil_win_rate"
]

columns = allowed_columns if st.session_state.logged_in_player != 'Tim' else allowed_columns + admin_columns
df = df[columns]

df = df[df["games"] >= min_games]

st.dataframe(df, use_container_width=True)

selection = st.pills("Darstellung", columns[1:], selection_mode="multi")
st.bar_chart(df, x="player", y=selection, stack=False)