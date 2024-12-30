
import streamlit as st
import pandas as pd
from streamlit_utils.utilities import get_image, load_scripts
import json
scripts = load_scripts()

all_town = [script.town for script in scripts]
all_town = list(set([role for roles in all_town for role in roles]))
all_outsider = [script.outsider for script in scripts]
all_outsider = list(set([role for roles in all_outsider for role in roles]))
all_minion = [script.minion for script in scripts]
all_minion = list(set([role for roles in all_minion for role in roles]))
all_demon = [script.demon for script in scripts]
all_demon = list(set([role for roles in all_demon for role in roles]))

with st.expander(label="Charakterfilter"):
    role_select_all = st.multiselect("Alle", all_town+all_outsider+all_minion+all_demon, placeholder="Rolle Suchen oder Auswählen", key="role_select_s0")
    role_select_1 = st.multiselect("Bürger", all_town, placeholder="Rolle Suchen oder Auswählen", key="role_select_s1")
    role_select_2 = st.multiselect("Außenseiter", all_outsider , placeholder="Rolle Suchen oder Auswählen", key="role_select_s2")
    role_select_3 = st.multiselect("Minions", all_minion , placeholder="Rolle Suchen oder Auswählen", key="role_select_s3")
    role_select_4 = st.multiselect("Demons", all_demon , placeholder="Rolle Suchen oder Auswählen", key="role_select_s4")

name, author, roles,download = st.columns(4)
name.markdown("### Name")
author.markdown("### Autor")
roles.markdown("### Rollen")
download.markdown("### Download")
scripts.sort(key=lambda x: x.name)
for i,script in enumerate(scripts):
    filtered = False
    for r in role_select_all + role_select_1 + role_select_2 + role_select_3 + role_select_4:
        if not script.contains_role(r):
            filtered = True
            break
    if filtered:
        continue
    name, author, roles,download = st.columns(4)
    name.text(script.name)
    author.text(script.author)
    popover = roles.popover("Rollen")
    for role_list in [script.town, script.outsider, script.minion, script.demon]:
        c1,c2,c3,c4 = popover.columns(4)    
        for j,role in enumerate(role_list):
            img = get_image(role)
            if j % 4 == 0:
                c1.image(img)
            elif j % 4 == 1:
                c2.image(img)
            elif j % 4 == 2:
                c3.image(img)
            else:
                c4.image(img)

    download.download_button(label="JSON", data=json.dumps(script.json_dict), mime="application/json", file_name=f"{script.name}.json", key=i)

