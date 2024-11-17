
import streamlit as st

from streamlit_utils.charts import get_winstreaks

st.title("Fun Facts")

game_data = st.session_state.game_data

st.divider()
st.header("Längste Siegesserie")

longest_streaks = get_winstreaks(game_data)

evil_streak = longest_streaks[longest_streaks["streak_team"] == "Böse"]
good_streak = longest_streaks[longest_streaks["streak_team"] == "Gut"]
col1, col2 = st.columns(2)
# col1,col2,col3,col4 = st.columns(4)
col1.subheader("Böse", divider="red")
col1.metric("Länge", f"{evil_streak['streak_length'].tolist()[0]} Siege")
col1.metric("Von:", f"{evil_streak['streak_start_date'].tolist()[0]}")
if evil_streak["is_ongoing"].tolist()[0]:
    col1.metric("Bis:", f"Heute")
else:
    col1.metric("Bis:", f"{evil_streak['streak_end_date'].tolist()[0]}")

st.divider()
col2.subheader("Gut", divider="blue")

col2.metric("Länge", f"{good_streak['streak_length'].tolist()[0]} Siege")
col2.metric("Von:", f"{good_streak['streak_start_date'].tolist()[0]}")
if good_streak["is_ongoing"].tolist()[0]:
    col2.metric("Bis:", f"Heute")
else:
    col2.metric("Bis:", f"{good_streak['streak_end_date'].tolist()[0]}")