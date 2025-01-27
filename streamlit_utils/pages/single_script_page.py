

import json
from streamlit_utils.utilities import get_english_name, get_image, get_role_text, load_scripts

import streamlit as st

wiki_base_path = "https://wiki.bloodontheclocktower.com/"

scripts = load_scripts()

if st.query_params.get("script", ""):
    script_name = st.query_params["script"]
else:
    script_name = st.selectbox("Skript", [script.name for script in scripts], placeholder="Skript auswählen", key="script_select")

if not script_name:
    st.stop()
script = [script for script in scripts if script.name == script_name][0]

def role_container(role, column):
    img = get_image(role)
    role_text = get_role_text(role)
    english_name = get_english_name(role)
    c1,c2,c3 = column.columns([0.15, 0.75, 0.1])
    c1.image(img, width=120)
    c2.markdown(f"""#### {role} \n  {role_text}""")
    c3.markdown(f"[Wiki]({wiki_base_path}{english_name.replace(' ', '_')})")
    

st.markdown(f"## {script.name}")
author,overview,download = st.columns(3)
author.markdown(f"### **Autor:** {script.author}")
download.download_button(label="JSON", data=json.dumps(script.json_dict), mime="application/json", file_name=f"{script.name}.json")
popover = overview.popover("Übersicht")
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


for role_list in [script.town, script.outsider, script.minion, script.demon]: 
    st.divider()  
    for j,role in enumerate(role_list):
        role_container(role, st)