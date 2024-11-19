import streamlit as st
from streamlit_utils.filter_elements import apply_filters, create_filters
from streamlit_utils.utilities import get_image
from streamlit_utils.filters import filter_range, get_aggregated_role_data
from st_clickable_images import clickable_images

full_data = st.session_state.full_data


st.subheader("Rollenübersicht (Siege/Spiele)")
###################################################### FILTER ##############################################
with st.expander("Filter", expanded=False):
    filters = create_filters(["Skript", "Erzähler", "Spieleranzahl", "Datum", "Rollentyp"], full_data)
    filtered_role_data = apply_filters(filters, full_data)
 
    
    aggregated_role_data = get_aggregated_role_data(filtered_role_data)

    if not aggregated_role_data.empty:
        max_games = aggregated_role_data["number_of_games"].max()
        game_count_select = st.select_slider("Spielanzahl", range(0,max_games+1), value=(0,max_games))

        sort_agg = st.pills("Sortieren nach", ["Siegrate", "Spielanzahl"], default="Spielanzahl")
        asc = st.pills("asc_sort", ["Abwärts", "Aufwärts"], default="Abwärts",label_visibility='collapsed')
        sort_dir = True if asc == 'Aufwärts' else False
        if sort_agg == 'Spielanzahl':
            aggregated_role_data = aggregated_role_data.sort_values(by='number_of_games', ascending=sort_dir)
        else:
            aggregated_role_data = aggregated_role_data.sort_values(by='winrate', ascending=sort_dir)

        aggregated_role_data = filter_range(game_count_select, "number_of_games", aggregated_role_data)

######################################################## Images and Overview #################################################
columns = []
for i in range(int(len(aggregated_role_data.index)/3)+1):
    columns += st.columns(3)

for col, r in zip(columns, list(aggregated_role_data.iloc[::1].itertuples(index=False, name=None))) :
    tile = col.container(height=120, border=True)
    c1, c2 = tile.columns([0.4,0.6], vertical_alignment="center")
    with c1:
        clicked_image = clickable_images(
            [get_image(r[0])],
            titles=[r[0]],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "0px", "height": "80px", "width": "80px"},
        )
    if clicked_image != -1:
        st.session_state.clicked_role = r[0]
        st.switch_page("streamlit_utils/pages/single_role_page.py")
        
    c2.html((f"<b>{r[0]}</b><br>{r[2]}/{r[1]}<br>({round(r[3]*100,2)}%)"))

