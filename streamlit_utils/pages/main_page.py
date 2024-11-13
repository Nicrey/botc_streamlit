import streamlit as st

from streamlit_app import create_multiselect, load_data
from streamlit_utils.charts import create_bar_chart, create_gamecount_charts, create_grouped_winrate_chart, create_playercount_over_time_chart, create_script_line_chart, create_winrate_over_time_chart
from streamlit_utils.filters import filter_date_range, filter_value_list

game_data = st.session_state.game_data


col1, col2, col3 = st.columns(3)
games = len(game_data.index)
good_wins = (game_data['win'] == 'Gut').sum()
evil_wins = games - good_wins
with col1:
    st.metric("Gespielte Spiele", games)
with col2:
    st.metric("Gute Siege", f"{good_wins} ({round(good_wins/games * 100,2)}%)")
with col3:
    st.metric("Böse Siege", f"{evil_wins} ({round(evil_wins/games * 100,2)}%)")

with col1:
    st.metric("Erstes Spieldatum", game_data["formatted_date"].min())
with col2:
    st.metric("Letztes Spieldatum", game_data["formatted_date"].max())
with col3:
    st.metric("Spieltermine", game_data['formatted_date'].nunique())

game_filter = st.expander("Filter")
with game_filter:
    script_select = create_multiselect("Script", game_data, "script")
    st_select = create_multiselect("Erzähler", game_data, "storyteller")
    player_count_select = create_multiselect("Spieleranzahl", game_data, "playercount")
    date_select = st.select_slider("Datum", game_data["formatted_date"], value=(game_data["formatted_date"].min(),game_data["formatted_date"].max() ))

filtered_game_data = game_data
for filter, column in zip([script_select, st_select, player_count_select], ["script", "storyteller", "playercount"]):
    filtered_game_data = filter_value_list(filter, column, filtered_game_data)
filtered_game_data = filter_date_range(date_select, "formatted_date", filtered_game_data)


col1 = filtered_game_data["formatted_date"].unique()

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
