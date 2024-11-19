import streamlit as st

from streamlit_utils.data_transformations import full_data_to_player_data
from streamlit_utils.filter_elements import apply_filters, create_filters

if not st.session_state.logged_in_player:
    st.warning("Bitte einloggen :)")
    st.stop()

st.subheader("Spieler*innenübersicht")
min_games = st.select_slider("Minimum Spiele", range(50), value=10)
full_data = st.session_state.full_data


###################################################### FILTER ###############################################

with st.expander("Filter"):
    filters = create_filters(["Skript", "Erzähler", "Spieleranzahl", "Datum", "Spieler"], full_data)
filtered_game_data = apply_filters(filters, full_data)

###################################################### Chart ###############################################

df = full_data_to_player_data(filtered_game_data)
df = df[df["games"] >= min_games]

# st.dataframe(df, use_container_width=True)
columns = df.columns.tolist()
selection = st.pills("Darstellung", columns[1:], selection_mode="multi")
st.bar_chart(df, x="player", y=selection, stack=False)