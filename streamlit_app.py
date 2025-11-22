import streamlit as st
import subprocess

st.title("🧩 Maze Generator Hub")

st.write("Choose which maze generator to run:")

# Buttons for DFS and HAK
col1, col2 = st.columns(2)

with col1:
    if st.button("DFS Maze Generator"):
        subprocess.run(["python", "games/maze_DFS.py"])

with col2:
    if st.button("HAK Maze Generator"):
        subprocess.run(["python", "games/maze_HAK.py"])
