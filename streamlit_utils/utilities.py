import json
import streamlit as st
import pandas as pd
from st_files_connection import FilesConnection

from streamlit_utils.objects.script import Script

GAME_DATA = "stats/game_data.csv"
PLAYER_ROLE_DATA = "stats/player_role_data.csv"

def login_player(password):
    return st.secrets.player_passwords.get(password, "")

def get_image(role_name):
    return st.session_state.characters[role_name]["image"][0]

def load_character_file(file_path):
    conn = st.connection('gcs', type=FilesConnection)
    with conn.open(f"botc_status_fulda/{file_path}", mode='r', encoding='utf-8') as file:
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

@st.cache_data
def load_scripts():
    conn = st.connection('gcs', type=FilesConnection)
    scripts = []
    for file in conn.fs.ls("botc_status_fulda/scripts"):
        if file.endswith(".json"):
            with conn.open(f"{file}", mode='r', encoding='utf-8') as file:
                data = json.load(file) 
                scripts.append(Script(data, str(file)))
    return scripts


def map_player_role_name(role):
    with open("data/name_mapping.json", 'r', encoding='utf-8') as file:
        data = json.load(file) 
    if role in data:
        return data[role]
    return role

def load_game_data():
    try:
        conn = st.connection('gcs', type=FilesConnection)
        with conn.open(f"botc_status_fulda/{GAME_DATA}", mode='r', encoding='utf-8') as file:
            game_data = pd.read_csv(file)
        game_data["formatted_date"] = game_data["date"].apply(lambda x: f"20{x.split('.')[2]}-{x.split('.')[1]}-{x.split('.')[0]}")
    except Exception as e:
        print(e)
        game_data = None
    return game_data

def load_full_data(game_dataset):
    try:
        conn = st.connection('gcs', type=FilesConnection)
        with conn.open(f"botc_status_fulda/{PLAYER_ROLE_DATA}", mode='r', encoding='utf-8') as file:
            player_role_data = pd.read_csv(file)
        
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

def hash_value(name):
    if not st.session_state.logged_in_player:
        return "***"
    return name

def load_data():
    game_data = load_game_data()
    full_data = load_full_data(game_data)
    if not st.session_state.logged_in_player:
        game_data["storyteller"] = game_data["storyteller"].apply(hash_value)
        full_data["storyteller"] = full_data["storyteller"].apply(hash_value)
    full_data["player"] = full_data["player"].apply(hash_value)
    return game_data, full_data

def get_english_name(german_name):
    remappings = {
        "fortuneteller": "Fortune_Teller",
        "snakecharmer": "Snake_Charmer",
        "town_crier": "Town_Crier",
        "tea_lady": "Tea_Lady",
        "devils_advocate": "Devil's_Advocate",
        "pit-hag": "Pit-Hag",
        "scarletwoman": "Scarlet_Woman",
        "evil_twin": "Evil_Twin",
        "no_dashii": "No_Dashii",
        "fanggu": "Fang_Gu",
        "bountyhunter": "Bounty_Hunter",
        "cult_leader": "Cult_Leader",
        "highpriestess": "High_Priestess",
        "villageidiot": "Village_Idiot",
        "poppygrower": "Poppy_Grower",
        "plaguedoctor": "Plague_Doctor",
        "organ_grinder": "Organ_Grinder",
        "alhadikhia": "Al-Hadikhia",
        "lilmonsta": "Lil'_Monsta",
        "lordoftyphon" :"Lord_of_Typhon"
    }
    english_name = st.session_state.characters[german_name]["id"].replace("de_DE_", "")
    return remappings.get(english_name, english_name)

def get_role_text(german_name):
    return st.session_state.characters[german_name]["ability"]
