"""
Author: Frank Kusel (frank-kusel)
Date Created: 27-01-2024
Date Modified: 05-02-2024

MIT License

Copyright (c) 2024 Frank Kusel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN 
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

F1 Pole Predictor.
To run the app, install all dependencies listed below. 
In the terminal of the project directory run: streamlit run F1.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime
import numpy as np
import sqlite3
from functions.plot import plot_cumulative_points
import functions.authenticate as auth

# ---------------------- SETTINGS ----------------------
race_results = []
page_title = "F1 POLE PREDICTOR"
page_icon = ':racing_car:'
layout = 'centered'
# ------------------------------------------------------

# ---------------------- DATABASE ----------------------
# TODO: Link these lists to the ERGAST API - or just update manually
# TODO: Set the month automatically for each race - user won't need to select circuit
driver_names = ("Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Zhou Guanyu", "Oscar Piastri", "Sergio Perez", "Charles Leclerc", "Daniel Ricciardo", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso", "Esteban Ocon", "Sebastian Vettel", "Lance Stroll", "Yuki Tsunoda", "George Russell", "Alex Albon", "Logan Sergeant", "Kevin Magnussen", "Nico Hulkenberg")
circuit_names = ("Bahrain International Circuit", "Jeddah Street Circuit", "Albert Park Circuit", "Suzuka Circuit", "Shanghai International Circuit", "Hard Rock Stadium Circuit", "Autodromo Enzo e Dino Ferrari", "Circuit de Monaco", "Circuit Gilles Villeneuve", "Circuit de Barcelona-Catalunya", "Red Bull Ring", "Silverstone Circuit", "Hungaroring", "Circuit de Spa-Francorchamps", "Circuit Zandvoort", "Autodromo Nazionale di Monza", "Baku City Circuit", "Marina Bay Street Circuit", "Circuit of the Americas", "Autódromo Hermanos Rodríguez", "Autódromo José Carlos Pace", "Las Vegas Strip Circuit", "Losail International Circuit", "Yas Marina Circuit")
# ------------------------------------------------------

# --- MAIN APP ---
def main():
    
    # Connect to database
    # TODO: Update and clean this database - figure out how to edit this
    # TODO: Possibly update this to a JSON file to make it easier to edit and query(?)
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    
    
    # Page info
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_icon + " " + page_title + " " + page_icon)
         
            
    # Login
    username, logged_in = auth.login() # returns username if logged in, otherwise returns None 
    
    
    # Rules
    with st.sidebar:
        with st.container():
            with st.expander("Racing Rules"):
                st.markdown('_Welcome to the F1 Prediction Game! Predict the 10th place driver and earn points._')
                points_system = {
                    "Position": ["10th", "11th", "9th", "12th", "8th", "13th", "7th"],
                    "Points": [25, 18, 15, 12, 8, 5, 2]
                }
                df_points_system = pd.DataFrame(points_system)
                st.dataframe(points_system, hide_index=True, use_container_width=True)
          
 
    # Log user's guesses
    if logged_in:    
        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                driver1 = st.selectbox(f':green[First] Pick:', sorted(driver_names), key="driver1")
            with col2:
                driver2 = st.selectbox(f':orange[Second] Pick:', sorted(driver_names), key="driver2")
            
            # TODO: sort the circuit names by date
            # TODO: select circuit automatically
            circuit = st.selectbox("Circuit:", sorted(circuit_names), key="circuit_ID")
            submitted = st.form_submit_button("Place your bet!")

        # 
        if submitted:
            driver1 = st.session_state["driver1"]
            driver2 = st.session_state["driver2"]
            st.success("I can't believe you've done this :0")
            st.balloons()
            # TODO: update a a database with the user's guess
            auth.save_user_guesses(username, driver1, driver2, circuit)
 
                
    # Metrics
    # TODO: Link these metrics to actual data from the dataframe
    if logged_in: 
        with st.container(border=False):
            current_position, current_points, leader_points = st.columns(3)
            current_position.container(height=120).metric("Current Position", 10, -5)
            current_points.container(height=120).metric("Current Points", 98, 12)
            leader_points.container(height=120).metric("Leader Points", 125, 25)


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
