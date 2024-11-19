import streamlit as st
from streamlit_utils.filter_elements import apply_filters, create_filters, create_multiselect, create_range_slider
from streamlit_utils.charts import create_role_bar_chart, create_role_rolling_winrate_chart, create_role_winrate_chart
from streamlit_utils.utilities import get_image
from streamlit_utils.filters import filter_value_list

full_data = st.session_state.full_data

########################################################## Role Selection & metrics ###############################################
st.subheader("Rollenübersicht (Siege/Spiele)")

# Role overview
roles = sorted(full_data["role"].unique().tolist())

role_select_r = st.selectbox("Rolle", roles, index=None, placeholder="Rolle Suchen oder Auswählen", key="role_select")

if "clicked_role" in st.session_state and st.session_state.clicked_role and role_select_r is None: 
    role_select_r =st.session_state.clicked_role

# Metrics
filtered_role_data = full_data
filtered_role_data = filter_value_list([role_select_r], "role", filtered_role_data)
first_date = filtered_role_data["formatted_date"].min()
last_date = filtered_role_data["formatted_date"].max()
if role_select_r:
    col1, col2, col3, col4,col5 = st.columns([0.15,0.25,0.2, 0.2,0.25], vertical_alignment="center")
    col1.subheader("**Rolle:**")
    col2.image(get_image(role_select_r), width=120)
    games = len(filtered_role_data.index)
    col3.metric("Anzahl Spiele", value=games)
    wins = (filtered_role_data["player_result"] == 'Win').sum()
    col4.metric("Siege", value=wins)
    col5.metric("Siegrate", value=f"{round(wins/games*100,2)} %")
    col1,col2 = st.columns(2)
    col1.metric("Zuerst gespielt", first_date)
    col2.metric("Zuletzt gespielt", last_date)

########################################################## Filter ###############################################
with st.expander("Filter", expanded=False):
    if not filtered_role_data.empty:
        filters = create_filters(["Erzähler", "Spieleranzahl", "Datum"], filtered_role_data)
        filtered_role_data = apply_filters(filters, filtered_role_data)

######################################################## CHARTS ###############################################
with st.expander("Vorkommen nach Datum", expanded=True):
    create_role_bar_chart(filtered_role_data, "formatted_date")

with st.expander("Vorkommen nach X", expanded=True):
    group_select = st.pills("Gruppieren nach:", ["Skript", "Erzähler", "Spieleranzahl"], default='Skript', key='group_role')
    create_role_bar_chart(filtered_role_data, group_select)

with st.expander("Siegrate nach X", expanded=True):
    group_select_2 = st.pills("Gruppieren nach:", ["Skript", "Erzähler", "Spieleranzahl"], default='Skript')
    create_role_winrate_chart(filtered_role_data, group_select_2)

with st.expander("Siegrate über Zeit", expanded=True):
    create_role_rolling_winrate_chart(filtered_role_data)

with st.expander("Spielerübersicht", expanded=True):
    create_role_bar_chart(filtered_role_data, "player")