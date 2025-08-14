# utils.py
import streamlit as st

def init_session():
    defaults = {
        "page": "home",
        "names": [],
        "selections": [],
        "current_player": 0,
        "selected_button": None,
        "mode": None,
        "room_code": None,
        "num_players": 0,
        "eliminated": None,
        "closest_to_avg": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
