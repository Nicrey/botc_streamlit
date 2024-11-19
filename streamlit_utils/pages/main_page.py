import streamlit as st

from streamlit_utils.charts import create_bar_chart, create_gamecount_charts, create_grouped_winrate_chart, create_playercount_over_time_chart, create_script_line_chart, create_winrate_over_time_chart

from streamlit_utils.filter_elements import apply_filters, create_filters

game_data = st.session_state.game_data

###################################################### FILTER ###############################################

with st.expander("Filter"):
    filters = create_filters(["Skript", "Erzähler", "Spieleranzahl", "Datum"], game_data)
filtered_game_data = apply_filters(filters, game_data)

####################################################### Metriken #################################

col1, col2, col3 = st.columns(3)
games = len(filtered_game_data.index)
good_wins = (filtered_game_data['win'] == 'Gut').sum()
evil_wins = games - good_wins
with col1:
    st.metric("Gespielte Spiele", games)
with col2:
    st.metric("Gute Siege", f"{good_wins} ({round(good_wins/games * 100,2)}%)")
with col3:
    st.metric("Böse Siege", f"{evil_wins} ({round(evil_wins/games * 100,2)}%)")

with col1:
    st.metric("Erstes Spieldatum", filtered_game_data["formatted_date"].min())
with col2:
    st.metric("Letztes Spieldatum", filtered_game_data["formatted_date"].max())
with col3:
    st.metric("Spieltermine", filtered_game_data['formatted_date'].nunique())

####################################################### Charts #################################

with st.expander(label="**Siege nach Team**", expanded=True):
    create_bar_chart(filtered_game_data)

with st.expander(label="**Gespielte Skripte**", expanded=True):
    create_script_line_chart(filtered_game_data)

with st.expander(label="**Siegesrate über Zeit**", expanded=True):
    create_winrate_over_time_chart(filtered_game_data)

with st.expander(label="**Spieleranzahl über Zeit**", expanded=True):
    create_playercount_over_time_chart(filtered_game_data)

with st.expander(label="**Siegesrate nach X**", expanded=True):
    pill_wr = st.pills("Gruppieren nach", ["Skript", "Spieleranzahl", "Erzähler"], default="Skript")
    create_grouped_winrate_chart(filtered_game_data, pill_wr)

with st.expander(label="**Spielanzahl nach X**", expanded=True):
    pill_gc = st.pills("Gruppieren nach", ["Skript", "Spieleranzahl", "Erzähler"], default="Skript", key="pill_gc")
    create_gamecount_charts(filtered_game_data, pill_gc)

st.subheader("Rohe Spieldaten")
st.dataframe(filtered_game_data)
