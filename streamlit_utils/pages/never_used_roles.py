
import streamlit as st
from streamlit_utils.utilities import get_image 

full_data = st.session_state.full_data
st.subheader("Nie genutzte Rollen")

role_type_map = {
    "Bürger": "townsfolk", 
    "Aussenseiter": "outsider", 
    "Scherge": "minion", 
    "Dämon": "demon"
}
role_types = role_type_map.keys()
type_sel = st.multiselect("Rollentyp",role_types , default=role_types)

origin_map ={
    "Experimental": "experimental",
    "Trouble Brewing": "tb", 
    "Bad Moon Rising": "bmr", 
    "Sects and Violets": "snv"
}
scripts = origin_map.keys()
origin_sel = st.multiselect("Herkunft", scripts, scripts)


used_roles = full_data["role"].unique().tolist()
unused_roles = []
for character in st.session_state.characters.values():
  
    if "edition" not in character:
        continue
    if "team" not in character:
        continue
    if character["team"] not in [role_type_map[t] for t in type_sel]:
        continue
    if character["edition"] not in [origin_map[o] for o in origin_sel]:
        continue

    if character["name"] not in used_roles:
        unused_roles.append(character["name"])

col1, col2 = st.columns(2)
with col1:
    st.metric("Nie gespielte Rollen", len(unused_roles))
with col2:
    st.metric("Gespielte Rollen", len(used_roles))
columns = []
for i in range(int(len(unused_roles)/4)+1):
    columns += st.columns(4)

for col, char in zip(columns, unused_roles):
    col.image(get_image(char), caption=char, width=120)