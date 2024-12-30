import streamlit as st
from streamlit_utils.utilities import load_characters, load_data, login_player
from streamlit_utils.filters import combine_tb, filter_kaboom, filter_teensies

st.title("Blood on the Clocktower Statistiken")
st.session_state.logged_in_player = ""
st.session_state.characters = load_characters()

############################ SIDEBAR ###########################
with st.sidebar:
    st.subheader("Spieler-Login", help="Spielerpasswort bei Tim erfragen. Passwort eingeben und Enter drücken, um Spieler*innenstatistiken zu sehen.", divider="rainbow")
    player_key = st.text_input("Spielerpasswort", "",type="password", label_visibility="collapsed")
    if player_key:
        st.session_state.logged_in_player = login_player(player_key)

    if st.session_state.logged_in_player:
        st.write(f"Willkommen {st.session_state.logged_in_player}!")
        
    st.subheader("Globale Filter", divider="rainbow")
    filter_kaboom_check = st.checkbox("Filter Kaboom", True)
    filter_teensies_check = st.checkbox("Filter Teensies (< 7 Spieler)", True)
    combine_tb_variants = st.checkbox("Trouble Brewing Varianten zusammenfassen", True)


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
pages= {
    "Allgemein": [
        st.Page("streamlit_utils/pages/main_page.py", title="Allgemein"),
        st.Page("streamlit_utils/pages/misc_page.py", title="Fun Facts"),
        st.Page("streamlit_utils/pages/script_page.py", title="Skripte")
    ],
    "Rollen": [
        st.Page("streamlit_utils/pages/role_page.py", title="Übersicht"),
        st.Page("streamlit_utils/pages/never_used_roles.py", title="Nie benutzte Rollen"),
        st.Page("streamlit_utils/pages/single_role_page.py", title="Einzelübersicht"),
    
    ],
    "Spieler*innen": [
        st.Page("streamlit_utils/pages/player_page.py", title="Übersicht"),
        st.Page("streamlit_utils/pages/single_player_page.py", title="Einzelübersicht"),
    ]
}
pg = st.navigation(pages)
pg.run()



