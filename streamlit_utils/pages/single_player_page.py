import streamlit as st

from streamlit_utils.utilities import get_image
from streamlit_app import create_multiselect
from streamlit_utils.filters import filter_date_range, filter_value_list
from streamlit_utils.charts import create_player_role_dist_chart, create_role_bar_chart, create_winrate_over_time_chart, create_winrate_over_time_chart_player, highlight_player_result

if not st.session_state.logged_in_player:
    st.warning("Nicht als Spieler eingeloggt, bitte Spielerpasswort eingeben")
    st.stop()

st.subheader("Einzelspieler*innenübersicht")

full_data = st.session_state.full_data
player = st.session_state.logged_in_player
if player == "Tim":
    player = st.selectbox("Spielerauswahl", full_data["player"].unique().tolist())

filtered_data = full_data[full_data["player"] == player]
if filtered_data.empty:
    st.stop()
with st.expander("Filter", expanded=False):
    if not filtered_data.empty:
        script_select_r = create_multiselect("Script ", filtered_data, "script")
        st_select_r = create_multiselect("Erzähler ", filtered_data, "storyteller")
        team_select = create_multiselect("Team ", filtered_data, "team")
        type_select = create_multiselect("Rollentyp", filtered_data, "role_type")
        role_select = create_multiselect("Rolle", filtered_data, "role")
        
        player_count_select_r = create_multiselect("Spieleranzahl ", filtered_data, "playercount")
        date_select_r = st.select_slider("Datum ", filtered_data["formatted_date"], value=(filtered_data["formatted_date"].min(),filtered_data["formatted_date"].max() ))

        for filter, column in zip([st_select_r, player_count_select_r, script_select_r, team_select, type_select, role_select], ["storyteller", "playercount", "script", "team", "role_type", "role"]):
            filtered_data = filter_value_list(filter, column, filtered_data)
        filtered_data = filter_date_range(date_select_r, "formatted_date", filtered_data)
if filtered_data.empty:
    st.stop()
games = len(filtered_data.index)
wins = (filtered_data["player_result"] == "Win").sum()
win_rate = wins/games

col1, col2, col3, col4 = st.columns(4)     
col1.metric("Statistiken für", player)
col2.metric("Spiele", games)
col3.metric("Siege", wins)
col4.metric("Siegesrate", f"{round(wins/games*100,2)} %")
st.subheader("Rohdaten")
dataframe_data = filtered_data[["date", "role", "player_result", "team", "script", "storyteller", "playercount"]]
styled_df = dataframe_data.style.apply(highlight_player_result, axis=1)
st.dataframe(styled_df, use_container_width=True, hide_index=True)

st.subheader("Gespielte Skripte")
create_role_bar_chart(df=filtered_data, column="script")

st.subheader("Sonstige Statistiken")

st.subheader("Ziehrate")
col1,col2,col3,col4 = st.columns(4)

town_games = (filtered_data["role_type"] == "townsfolk").sum()
outsider_games = (filtered_data["role_type"] == "outsider").sum()
minion_games = (filtered_data["role_type"] == "minion").sum()
demon_games = (filtered_data["role_type"] == "demon").sum()
demon_games = 0 if not demon_games else demon_games

good_games = town_games + outsider_games
evil_games = minion_games + demon_games
col1.metric("Bürger", f"{town_games} ({round(town_games/games*100)} %)")
col2.metric("Aussenseiter", f"{outsider_games} ({round(outsider_games/games*100)} %)")
col3.metric("Scherge", f"{minion_games} ({round(minion_games/games*100)} %)")
col4.metric("Dämon", f"{demon_games} ({round(demon_games/games*100)} %)")
col2.metric("Gut", f"{good_games} ({round(good_games/games*100)} %)")
col3.metric("Böse", f"{evil_games} ({round(evil_games/games*100)} %)")

st.subheader("Siegesrate")
col1,col2,col3,col4 = st.columns(4)
town_wins = ((filtered_data["role_type"] == "townsfolk") & (filtered_data["player_result"] == "Win")).sum()
outsider_wins = ((filtered_data["role_type"] == "outsider") & (filtered_data["player_result"] == "Win")).sum()
minion_wins = ((filtered_data["role_type"] == "minion") & (filtered_data["player_result"] == "Win")).sum()
demon_wins = ((filtered_data["role_type"] == "demon") & (filtered_data["player_result"] == "Win")).sum()
demon_wins = 0 if not demon_wins else demon_wins
good_wins = town_wins + outsider_wins
evil_wins = minion_wins + demon_wins
col1.metric("Als Bürger", f"{town_wins} ({round(town_wins/town_games*100)} %)")
col2.metric("Als Aussenseiter", f"{outsider_wins} ({round(outsider_wins/outsider_games*100)} %)")
col3.metric("Als Scherge", f"{minion_wins} ({round(minion_wins/minion_games*100)} %)")
if demon_games > 0:
    col4.metric("Als Dämon", f"{demon_wins} ({round(demon_wins/demon_games*100)} %)")
col2.metric("Als Gut",f"{good_wins} ({round(good_wins/good_games*100)} %)")
col3.metric("Als Böse",f"{evil_wins} ({round(evil_wins/evil_games*100)} %)")

st.subheader("Siegesrate über Zeit")
create_winrate_over_time_chart_player(filtered_data)
st.subheader("Rollenverteilung")
create_player_role_dist_chart(filtered_data)

st.subheader("Noch nie gespielte Rollen")

role_type_map = {
    "Bürger": "townsfolk", 
    "Aussenseiter": "outsider", 
    "Scherge": "minion", 
    "Dämon": "demon"
}
role_types = role_type_map.keys()
type_sel = st.multiselect("Rollentyp",role_types , default=role_types)

origin_map ={
    "Experimental": "experimental",
    "Trouble Brewing": "tb", 
    "Bad Moon Rising": "bmr", 
    "Sects and Violets": "snv"
}
scripts = origin_map.keys()
origin_sel = st.multiselect("Herkunft", scripts, scripts)


used_roles = full_data[full_data["player"] == player]["role"].unique().tolist()
unused_roles = []
for character in st.session_state.characters.values():
  
    if "edition" not in character:
        continue
    if "team" not in character:
        continue
    if character["team"] not in [role_type_map[t] for t in type_sel]:
        continue
    if character["edition"] not in [origin_map[o] for o in origin_sel]:
        continue

    if character["name"] not in used_roles:
        unused_roles.append(character["name"])

col1, col2 = st.columns(2)
with col1:
    st.metric("Nie gespielte Rollen", len(unused_roles))
with col2:
    st.metric("Gespielte Rollen", len(used_roles))
columns = []
for i in range(int(len(unused_roles)/4)+1):
    columns += st.columns(4)

for col, char in zip(columns, unused_roles):
    col.image(get_image(char), caption=char, width=120)



