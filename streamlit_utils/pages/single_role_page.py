import streamlit as st

from streamlit_utils.charts import create_role_bar_chart, create_role_rolling_winrate_chart, create_role_winrate_chart
from streamlit_utils.utilities import get_image
from streamlit_app import create_multiselect
from streamlit_utils.filters import filter_date_range, filter_value_list

full_data = st.session_state.full_data

st.subheader("Rollenübersicht (Siege/Spiele)")
roles = full_data["role"].unique().tolist()
role_select_r = st.selectbox("Rolle", roles, index=None, placeholder="Rolle Suchen oder Auswählen")
filtered_role_data = full_data
filtered_role_data = filter_value_list([role_select_r], "role", filtered_role_data)

if role_select_r:
    col1, col2, col3, col4,col5 = st.columns([0.15,0.25,0.2, 0.2,0.25], vertical_alignment="center")
    col1.subheader("**Rolle:**")
    col2.image(get_image(role_select_r), width=120)
    games = len(filtered_role_data.index)
    col3.metric("Anzahl Spiele", value=games)
    wins = (filtered_role_data["player_result"] == 'Win').sum()
    col4.metric("Siege", value=wins)
    col5.metric("Siegrate", value=f"{round(wins/games*100,2)} %")


with st.expander("Filter", expanded=False):
    if not filtered_role_data.empty:
        st_select_r = create_multiselect("Erzähler ", filtered_role_data, "storyteller")
        player_count_select_r = create_multiselect("Spieleranzahl ", filtered_role_data, "playercount")
        date_select_r = st.select_slider("Datum ", filtered_role_data["formatted_date"], value=(filtered_role_data["formatted_date"].min(),filtered_role_data["formatted_date"].max() ))

        for filter, column in zip([st_select_r, player_count_select_r], ["storyteller", "playercount"]):
            filtered_role_data = filter_value_list(filter, column, filtered_role_data)
        filtered_role_data = filter_date_range(date_select_r, "formatted_date", filtered_role_data)

with st.expander("Vorkommen nach Datum", expanded=True):
    create_role_bar_chart(filtered_role_data, "formatted_date")

with st.expander("Vorkommen nach X", expanded=True):
    group_select = st.pills("Gruppieren nach:", ["Skript", "Erzähler", "Spieleranzahl"], default='Skript', key='group_role')
    create_role_bar_chart(filtered_role_data, group_select)

with st.expander("Siegrate nach X", expanded=True):
    group_select_2 = st.pills("Gruppieren nach:", ["Skript", "Erzähler", "Spieleranzahl"], default='Skript')
    create_role_winrate_chart(filtered_role_data, group_select_2)
# Filter Rolle mit Suchfunktion?

with st.expander("Siegrate über Zeit", expanded=True):
    create_role_rolling_winrate_chart(filtered_role_data)

with st.expander("Spielerübersicht", expanded=True):
    create_role_bar_chart(filtered_role_data, "player")