import numpy as np
import pandas as pd
import streamlit as st

# --- Game Setup ---
if "sea" not in st.session_state:
    st.session_state.sea = np.random.randint(1, 10, size=(100, 100))

if "rounds" not in st.session_state:
    st.session_state.rounds = 5

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "current_round" not in st.session_state:
    st.session_state.current_round = 1

if "current_player" not in st.session_state:
    st.session_state.current_player = 1

if "noofusers" not in st.session_state:
    st.session_state.noofusers = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

# --- Game Functions ---
def play_round():
    """Simulate fishing round for current player"""
    row = np.random.randint(0, 100)
    col = np.random.randint(0, 100)
    points = st.session_state.sea[row][col]

    player = st.session_state.current_player
    if player not in st.session_state.scores:
        st.session_state.scores[player] = 0
    st.session_state.scores[player] += points

    st.session_state.current_round += 1

    if st.session_state.current_round > st.session_state.rounds:
        st.session_state.current_round = 1
        st.session_state.current_player += 1

    if st.session_state.current_player > st.session_state.noofusers:
        st.session_state.game_over = True

    st.session_state.last_catch = points

# --- UI ---
st.title("🎣 Fishing Game")
st.write("Catch as many fish as you can in your turns!")

# Input number of players at start
if st.session_state.noofusers == 0:
    noofusers = st.number_input("How many anglers are playing?", min_value=1, step=1)
    if st.button("Start Fishing"):
        st.session_state.noofusers = noofusers
        st.experimental_rerun()
else:
    if not st.session_state.game_over:
        st.subheader(f"🎣 Player {st.session_state.current_player}'s Turn")
        st.write(f"Round {st.session_state.current_round} of {st.session_state.rounds}")

        if st.button("Cast the Line 🎣"):
            play_round()
            st.experimental_rerun()

        # Show last catch
        if "last_catch" in st.session_state:
            st.write(f"🐟 Fish caught: {st.session_state.last_catch} points!")

        # Show current scores live
        if st.session_state.scores:
            st.write("📊 Current Catch Totals:")
            st.dataframe(pd.Series(st.session_state.scores).rename("Points"))

    else:
        st.success("🏁 Fishing Trip Over!")
        scores = pd.Series(st.session_state.scores).rename("Points")
        winner = scores.idxmax()
        st.write("🏆 Final Catch Totals:")
        st.dataframe(scores)
        st.success(f"🎉 Winner is Player {winner} with {scores[winner]} points! 🎣")

        if st.button("🔄 Start New Fishing Trip"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
