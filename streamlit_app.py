import streamlit as st
import pandas as pd
from streamlit_utils.utilities import load_characters, load_full_data, load_game_data, login_player
from streamlit_utils.filters import filter_kaboom, filter_teensies
from st_files_connection import FilesConnection

# @st.cache_data
def hash_value(name):
    if not st.session_state.logged_in_player:
        return "***"
    return name

# @st.cache_data
def load_data():
    game_data = load_game_data()
    full_data = load_full_data(game_data)
    if not st.session_state.logged_in_player:
        game_data["storyteller"] = game_data["storyteller"].apply(hash_value)
        full_data["storyteller"] = full_data["storyteller"].apply(hash_value)
    full_data["player"] = full_data["player"].apply(hash_value)
    return game_data, full_data

def create_multiselect(name, dataframe, column):
    values = dataframe[column].unique().tolist()
    return st.multiselect(name,values,values)

st.title("BOTC Fulda Stats")
st.session_state.logged_in_player = ""
st.session_state.characters = load_characters()

with st.sidebar:
    filter_kaboom_check = st.checkbox("Filter Kaboom", True)
    filter_teensies_check = st.checkbox("Filter Teensies (< 7 Spieler)", True)
    player_key = st.text_input("Spielerpasswort", "",type="password")
    if player_key:
        st.session_state.logged_in_player = login_player(player_key)

    if st.session_state.logged_in_player:
        st.write(f"Willkommen {st.session_state.logged_in_player}!")

game_data, full_data = load_data()

if filter_kaboom_check:
    game_data = filter_kaboom(game_data)
    full_data = filter_kaboom(full_data)

    
if filter_teensies_check:
    game_data = filter_teensies(game_data)
    full_data = filter_teensies(full_data)

st.session_state["game_data"] = game_data

st.session_state["full_data"] = full_data

pg = st.navigation([
    st.Page("streamlit_utils/pages/main_page.py", title="Allgemein"),
    st.Page("streamlit_utils/pages/role_page.py", title="Rollenübersicht"),
    st.Page("streamlit_utils/pages/never_used_roles.py", title="Nie benutzte Rollen"),
    st.Page("streamlit_utils/pages/single_role_page.py", title="Einzelrollenübersicht"),
    st.Page("streamlit_utils/pages/player_page.py", title="Spieler*innenübersicht"),
    st.Page("streamlit_utils/pages/single_player_page.py", title="Einzelspieler*innenübersicht"),
    st.Page("streamlit_utils/pages/misc_page.py", title="Fun Facts"),
    
    ])
pg.run()

