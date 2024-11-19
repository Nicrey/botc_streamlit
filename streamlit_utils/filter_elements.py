from dataclasses import dataclass
from typing import Any
import streamlit as st

from streamlit_utils.filters import filter_date_range, filter_value_list

@dataclass
class Filter:
    name: str
    column: str
    st_element: Any 

def create_multiselect(name, dataframe, column):
    values = dataframe[column].unique().tolist()
    return Filter(name, column, st.multiselect(name,values,values))

def create_range_slider(name, df, column):
    min = df[column].min()
    max = df[column].max()
    if min == max:
        return Filter(name, column, st.select_slider(name, df[column], value=min))
    else:
        return Filter(name, column, st.select_slider(name, df[column], value=(min, max)))
    
def create_filters(filter_name_list, df):
    filters = []
    for name in filter_name_list:
        if name == "Skript":
            filters.append(create_multiselect("Script", df, "script"))
        if name == "Erzähler":
            filters.append(create_multiselect("Erzähler", df, "storyteller"))
        if name == "Spieleranzahl":
            filters.append(create_multiselect("Spieleranzahl", df, "playercount"))
        if name == "Datum":
            filters.append(create_range_slider("Datum", df, "formatted_date"))
        if name == "Rollentyp":
            filters.append(create_multiselect("Rollentyp", df, "role_type"))
        if name == "Rolle":
            filters.append(create_multiselect("Rolle", df, "role"))
        if name == "Team":
            filters.append(create_multiselect("Team", df, "team"))
        if name == "Spieler":
            filters.append(create_multiselect("Spieler", df, "player"))
    return filters

def apply_filters(filters, df):
    filtered = df
    for filter in filters:
        if filter.column in  ["script", "storyteller", "playercount", "role_type", "role", "team", "player"]:
            filtered = filter_value_list(filter.st_element, filter.column, filtered)
        if filter.column == "formatted_date":
            filtered = filter_date_range(filter.st_element, filter.column, filtered)
    return filtered
