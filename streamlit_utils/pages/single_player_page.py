import streamlit as st

from streamlit_utils.utilities import create_multiselect, get_image
from streamlit_utils.filters import filter_date_range, filter_value_list
from streamlit_utils.charts import create_player_role_dist_chart, create_role_bar_chart, create_winrate_over_time_chart_player, get_player_winstreaks, highlight_player_result, GOOD_COLOR, EVIL_COLOR

if not st.session_state.logged_in_player:
    st.warning("Nicht als Spieler eingeloggt, bitte Spielerpasswort eingeben")
    st.stop()

st.subheader("Einzelspieler*innenübersicht")

full_data = st.session_state.full_data
player = st.session_state.logged_in_player
if player == "Tim":
    player = st.selectbox("Spielerauswahl", full_data["player"].unique().tolist())


##################################################### Filter ############################################
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


##################################################### General Stats ############################################
games = len(filtered_data.index)
wins = (filtered_data["player_result"] == "Win").sum()
win_rate = wins/games

col1, col2, col3, col4 = st.columns(4)     
col1.metric("Statistiken für", player)
col2.metric("Spiele", games)
col3.metric("Siege", wins)
col4.metric("Siegesrate", f"{round(wins/games*100,2)} %")

##################################################### Styled Raw Data ############################################
with st.expander("Rohdaten", expanded=True):
    dataframe_data = filtered_data[["date", "role", "player_result", "team", "script", "storyteller", "playercount"]]
    styled_df = dataframe_data.style.apply(highlight_player_result, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

##################################################### Gespielte Skripte ############################################
with st.expander("Gespielte Skripte", expanded=True):
    create_role_bar_chart(df=filtered_data, column="script")

##################################################### Draw/Winrates ############################################

with st.expander("Zieh und Siegesrate", expanded=True):
    st.subheader("Ziehrate")
    col1,col2, col3 = st.columns([0.2,0.3,0.3])
    col1.subheader("Rollentyp", divider="violet")
    col2.subheader("Spiele (Ziehrate)", divider="rainbow")
    col3.subheader("Siege (Siegesrate)", divider="green")

    rate_idx = ["townsfolk", "outsider", "minion", "demon", "good", "evil"]
    german = ["Bürger", "Aussenseiter", "Scherge", "Dämon", "Gut", "Böse"]
    colors = ["blue", "blue", "red", "red", "blue", "red"]
    game_count = {}
    game_rate = {}
    win_count = {}
    win_rate = {}
    col1.markdown(f"#### Gesamt:")
    col2.metric("Gesamt", games, label_visibility="collapsed")
    col3.metric("Gesamt", wins, label_visibility="collapsed")
    st.divider()
    for i,idx in enumerate(rate_idx):
        if idx == "good":
            st.divider()
            game_count[idx] = game_count["townsfolk"] + game_count["outsider"]
            win_count[idx] = win_count["townsfolk"] + win_count["outsider"]
        elif idx == "evil":
            game_count[idx] = game_count["minion"] + game_count["demon"]
            win_count[idx] = win_count["minion"] + win_count["demon"]
        else:
            game_count[idx] = (filtered_data["role_type"] == idx).sum()
            win_count[idx] = ((filtered_data["role_type"] == idx) & (filtered_data["player_result"] == "Win")).sum()
        game_count[idx] = game_count[idx] if game_count[idx] else 0
        win_count[idx] = win_count[idx] if win_count[idx] else 0

        win_rate[idx] = round(win_count[idx]/game_count[idx] * 100) if game_count[idx] > 0 else 0
        game_rate[idx] = round(game_count[idx] / games * 100)

        col1,col2,col3 = st.columns([0.2,0.3,0.3])
        col1.markdown(f"#### :{colors[i]}[{german[i]}]")
        col2.metric(label=f"Als {german[i]}", value=f"{game_count[idx]} ({game_rate[idx]} %)", label_visibility="collapsed")
        col3.metric(label=f"Als {german[i]}",value=f"{win_count[idx]} ({win_rate[idx]} %)", label_visibility="collapsed")


##################################################### Winrate over Time ############################################
with st.expander("Siegesrate über Zeit", expanded=True):
    create_winrate_over_time_chart_player(filtered_data)


##################################################### Serien ############################################
with st.expander("Längste Serien", expanded=True):
    longest_streaks = get_player_winstreaks(filtered_data)

    loss_streak = longest_streaks[longest_streaks["streak_team"] == "Loss"]
    win_streak = longest_streaks[longest_streaks["streak_team"] == "Win"]
    col1, col2 = st.columns(2)
    # col1,col2,col3,col4 = st.columns(4)
    col1.subheader("Niederlageserie", divider="gray")
    try:
        col1.metric("Länge", f"{loss_streak['streak_length'].tolist()[0]} Niederlagen")
        col1.metric("Von:", f"{loss_streak['streak_start_date'].tolist()[0]}")
        if loss_streak["is_ongoing"].tolist()[0]:
            col1.metric("Bis:", f"Heute")
        else:
            col1.metric("Bis:", f"{loss_streak['streak_end_date'].tolist()[0]}")
    except Exception as e:
        print(e)
        col2.warning("Zu wenige Spiele")

    st.divider()
    col2.subheader("Siegesserie", divider="green")
    try:
        col2.metric("Länge", f"{win_streak['streak_length'].tolist()[0]} Siege")
        col2.metric("Von:", f"{win_streak['streak_start_date'].tolist()[0]}")
        if win_streak["is_ongoing"].tolist()[0]:
            col2.metric("Bis:", f"Heute")
        else:
            col2.metric("Bis:", f"{win_streak['streak_end_date'].tolist()[0]}")
    except Exception as e:
        print(e)
        col2.warning("Zu wenige Spiele")

##################################################### Rollenverteilung ############################################
with st.expander("Rollenverteilung", expanded=True):
    create_player_role_dist_chart(filtered_data)


##################################################### Noch nie gespielte Rollen ############################################
with st.expander("Noch nie gespielte Rollen", expanded=True):
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



