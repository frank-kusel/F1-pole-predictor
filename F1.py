import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime
import numpy as np
import sqlite3
from plot import plot_cumulative_points
import authenticate as auth

# ---------------------- SETTINGS ----------------------
race_results = []
page_title = "F1 POLE PREDICTOR"
page_icon = ':racing_car:'
layout = 'centered'
# ------------------------------------------------------

# ---------------------- DATABASE ----------------------
driver_names = ("Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Sergio Perez", "Charles Leclerc", "Daniel Ricciardo", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso", "Esteban Ocon", "Sebastian Vettel", "Lance Stroll", "Yuki Tsunoda", "Kimi Raikkonen", "Antonio Giovinazzi", "George Russell", "Mick Schumacher", "Nikita Mazepin", "Nicholas Latifi")
circuit_names = ("Bahrain International Circuit", "Jeddah Street Circuit", "Albert Park Circuit", "Suzuka Circuit", "Shanghai International Circuit", "Hard Rock Stadium Circuit", "Autodromo Enzo e Dino Ferrari", "Circuit de Monaco", "Circuit Gilles Villeneuve", "Circuit de Barcelona-Catalunya", "Red Bull Ring", "Silverstone Circuit", "Hungaroring", "Circuit de Spa-Francorchamps", "Circuit Zandvoort", "Autodromo Nazionale di Monza", "Baku City Circuit", "Marina Bay Street Circuit", "Circuit of the Americas", "Autódromo Hermanos Rodríguez", "Autódromo José Carlos Pace", "Las Vegas Strip Circuit", "Losail International Circuit", "Yas Marina Circuit")
# ------------------------------------------------------

# --- MAIN APP ---
def main():
    
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    
    # --- Page Info ---
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_icon + " " + page_title + " " + page_icon)
    with st.container(border=False):
        with st.expander("Racing Rules"):
            st.markdown('_Welcome to the F1 Prediction Game! \
                Predict the 10th place driver and earn points._')
            
    # --- Login and record user's guess ---
    username = auth.login()        
    # st.subheader(f'Select your :red[drivers]... ')
    
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            driver1 = st.selectbox(f':green[First] Pick:', driver_names, key="driver1")
        with col2:
            driver2 = st.selectbox(f':orange[Second] Pick:', driver_names, key="driver2")
        
        # TODO: compare today's date with circuit date and return error if wrong circuit is chosen. Or just show the next race
        circuit = st.selectbox("Circuit:", circuit_names, key="circuit_ID")
        submitted = st.form_submit_button("Place your bet!")

        if submitted:
            driver1 = st.session_state["driver1"]
            driver2 = st.session_state["driver2"]
            st.success("I can't believe you've done this :0")
            st.balloons()
            # TODO: update a a database with the user's guess
            auth.save_user_guesses(username, driver1, driver2, circuit)


    # --- Metrics ---
    # TODO: Edit this to show the user's current position and change in position
    with st.container(border=False):
        current_position, current_points, leader_points = st.columns(3)
        current_position.container(height=120).metric("Current Position", 10, -5)
        current_points.container(height=120).metric("Current Points", 98, 12)
        leader_points.container(height=120).metric("Leader Points", 125, 25)

    # Function to fetch user guesses
    selected_circuit = st.selectbox("Filter by Circuit", circuit_names)
    c.execute("SELECT user_id, driver1, driver2, circuit FROM user_guesses WHERE circuit=?", (selected_circuit,))
    guesses_data = c.fetchall()
    df = pd.DataFrame(guesses_data, columns=['Name', 'Driver 1', 'Driver 2', 'Circuit'])
    st.write(df)


    # --- Load data ---
    df = pd.read_excel('F1_data.xlsm', sheet_name='Results', index_col=0)
    df = df.T
    cumulative_points = df.cumsum()

    # --- Plot cumulative points ---
    st.header("Leaderboard")
    
    plot_cumulative_points(cumulative_points)

# Run the app
if __name__ == "__main__":
    main()
