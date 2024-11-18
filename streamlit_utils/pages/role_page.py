import streamlit as st
from streamlit_utils.utilities import create_multiselect, get_image
from streamlit_utils.filters import filter_date_range, filter_range, filter_value_list, get_aggregated_role_data

full_data = st.session_state.full_data


st.subheader("Rollenübersicht (Siege/Spiele)")
with st.expander("Filter", expanded=False):
    script_select_r = create_multiselect("Script ", full_data, "script")
    st_select_r = create_multiselect("Erzähler ", full_data, "storyteller")
    player_count_select_r = create_multiselect("Spieleranzahl ", full_data, "playercount")
    date_select_r = st.select_slider("Datum ", full_data["formatted_date"], value=(full_data["formatted_date"].min(),full_data["formatted_date"].max() ))

    role_type_map = {
        "Bürger": "townsfolk", 
        "Aussenseiter": "outsider", 
        "Scherge": "minion", 
        "Dämon": "demon"
    }
    role_types = role_type_map.keys()
    type_sel = st.multiselect("Rollentyp",role_types , default=role_types)
    type_select = [role_type_map[t] for t in type_sel]


    filtered_role_data = full_data
    for filter, column in zip([script_select_r, st_select_r, player_count_select_r, type_select], ["script", "storyteller", "playercount", "role_type"]):
        filtered_role_data = filter_value_list(filter, column, filtered_role_data)
    filtered_role_data = filter_date_range(date_select_r, "formatted_date", filtered_role_data)
    

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

columns = []
for i in range(int(len(aggregated_role_data.index)/3)+1):
    columns += st.columns(3)

for col, r in zip(columns, list(aggregated_role_data.iloc[::1].itertuples(index=False, name=None))) :
    tile = col.container(height=120, border=True)
    c1, c2 = tile.columns([0.4,0.6], vertical_alignment="center")
    c1.image(get_image(r[0]),caption=f"", width=80)
    c2.html((f"<b>{r[0]}</b><br>{r[2]}/{r[1]}<br>({round(r[3]*100,2)}%)"))

