import json
import streamlit as st
import pandas as pd

GAME_DATA = "stats/game_data.csv"
PLAYER_ROLE_DATA = "stats/player_role_data.csv"

def login_player(password):
    
    return st.secrets.player_passwords.get(password, "")

def get_image(role_name):
    return st.session_state.characters[role_name]["image"][0]

def load_character_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file) 
    return data

@st.cache_data
def load_characters():
    characters = []
    characters += load_character_file("data/de_demons.json")
    characters += load_character_file("data/de_minions.json")
    characters += load_character_file("data/de_outsiders.json")
    characters += load_character_file("data/de_town.json")
    characters += load_character_file("data/de_travelers.json")
    for character in characters: 
        character["image"] = [character["image"], ""]
    character_dict = {character["name"]: character for character in characters}
    return character_dict

def map_player_role_name(role):
    with open("data/name_mapping.json", 'r', encoding='utf-8') as file:
        data = json.load(file) 
    if role in data:
        return data[role]
    return role

def load_game_data():
    try:
        game_data = pd.read_csv(GAME_DATA)
        game_data["formatted_date"] = game_data["date"].apply(lambda x: f"20{x.split('.')[2]}-{x.split('.')[1]}-{x.split('.')[0]}")
    except Exception as e:
        print(e)
        game_data = None
    return game_data

def load_full_data(game_dataset):
    try:
        player_role_data = pd.read_csv(PLAYER_ROLE_DATA)
    except Exception as e:
        print(e)
        return 
    # For alignment changing characters the end of game alignment is added as "| Böse" or "| Gut" at the end of the role
    # This second part of the role is then put into the team helper column 
    player_role_data["team_helper"] = player_role_data["role"].apply(lambda x: x.split("|")[1].strip() if len(x.split("|")) > 1 else None)
    player_role_data["role"] = player_role_data["role"].apply(lambda x: x.split("|")[0].strip())
    player_role_data["role"] = player_role_data["role"].apply(lambda x: map_player_role_name(x))
    player_role_data["role_type"] = player_role_data["role"].apply(lambda x: st.session_state.characters[x]["team"])
    player_role_data["team"] = player_role_data["role_type"].apply(lambda x: 'Böse' if x in ['minion', 'demon'] else 'Gut')
    player_role_data["team"] =player_role_data.apply((lambda x: x["team_helper"] if x["team_helper"] is not None else x["team"]), axis =1)
    player_role_data = player_role_data.drop("team_helper", axis=1)
    #
    full_dataset = player_role_data.merge(game_dataset, how='left', on='gameid')
    full_dataset["player_result"] = full_dataset.apply((lambda x: "Win" if x["win"] == x["team"] else "Loss"),axis=1)
    return full_dataset