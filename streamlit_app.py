import streamlit as st
from streamlit_utils.utilities import load_characters, load_data, login_player
from streamlit_utils.filters import combine_tb, filter_kaboom, filter_teensies

st.title("Blood on the Clocktower Statistiken")
st.session_state.logged_in_player = ""
st.session_state.characters = load_characters()

############################ SIDEBAR ###########################
with st.sidebar:
    filter_kaboom_check = st.checkbox("Filter Kaboom", True)
    filter_teensies_check = st.checkbox("Filter Teensies (< 7 Spieler)", True)
    combine_tb_variants = st.checkbox("Trouble Brewing Varianten zusammenfassen", True)
    player_key = st.text_input("Spielerpasswort", "",type="password")
    if player_key:
        st.session_state.logged_in_player = login_player(player_key)

    if st.session_state.logged_in_player:
        st.write(f"Willkommen {st.session_state.logged_in_player}!")


############################ DATA LOADING ###########################
game_data, full_data = load_data()

if filter_kaboom_check:
    game_data = filter_kaboom(game_data)
    full_data = filter_kaboom(full_data)
    
if filter_teensies_check:
    game_data = filter_teensies(game_data)
    full_data = filter_teensies(full_data)

if combine_tb_variants:
    game_data = combine_tb(game_data)
    full_data = combine_tb(full_data)

st.session_state["game_data"] = game_data
st.session_state["full_data"] = full_data


############################ NAVIGATION ###########################
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

