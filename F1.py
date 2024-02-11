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
import functions.database as db

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
    
    # Select database
    database = r"f1.db"
    conn = db.create_connection(database)
    
    # Page info
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_icon + " " + page_title + " " + page_icon)

    # Registration or Login selection
    option = st.sidebar.radio("Select Option:", ("Login", "Register"), key="register_or_login")
    
    # Retrieve user_id from session state
    user_id = st.session_state.get('user_id')
    logged_in = st.session_state.get('logged_in')
    
    # Login
    if user_id is None: # If user_id is not in session state, perform login

        if option == "Login":
            # Login
            username = st.sidebar.text_input("Username:")
            password = st.sidebar.text_input("Password:", type="password")
            logged_in = False
            
            if st.sidebar.button("Login"):
                user_id = db.authenticate_user(conn, (username, password))
                if not user_id == None:
                    st.sidebar.success("Login successful!")
                    logged_in=True
                    st.session_state['logged_in'] = logged_in
                    st.session_state['user_id'] = user_id
                else:
                    st.sidebar.error("Invalid username or password.")
                    logged_in=False
                    
        elif option == "Register":
            # Registration
            logged_in = False
            st.session_state['logged_in'] = logged_in
            new_username = st.sidebar.text_input("Enter new username:")
            new_password = st.sidebar.text_input("Enter new password:", type="password")
            
            if st.sidebar.button("Register"):
                if db.is_username_taken(conn, (new_username,)):
                    st.sidebar.warning("Username already taken. Please choose another one.")
                else:
                    user_id = db.register_user(conn, (new_username, new_password))
                    st.sidebar.success("Registration successful!")
        

    if logged_in:
        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                driver1 = st.selectbox(f':green[First] Pick:', sorted(driver_names), key="driver1")
            with col2:
                driver2 = st.selectbox(f':orange[Second] Pick:', sorted(driver_names), key="driver2")
            
            circuit = st.selectbox("Circuit:", sorted(circuit_names), key="circuit_ID")  
            submitted = st.form_submit_button("Place your bet!")

            # Save user guesses to a dataframe -> SQLite
            if submitted:
                current_user = st.session_state['user_id']
                db.save_user_guesses(conn, (current_user, driver1, driver2, circuit))
                st.write(f'You have selected :green[{driver1}] and :orange[{driver2}]')
    
    
        # Metrics
        with st.container(border=False):
            current_position, current_points, leader_points = st.columns(3)
            current_position.container(height=120).metric("Current Position", 10, -5)
            current_points.container(height=120).metric("Current Points", 98, 12)
            leader_points.container(height=120).metric("Leader Points", 125, 25)
    
    
        
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
    
    
    if logged_in:   
        # Function to fetch user guesses
        c = conn.cursor()
        c.execute("SELECT user_id, driver1, driver2, circuit FROM user_guesses")
        guesses_data = c.fetchall()

        df = pd.DataFrame(guesses_data, columns=['Name', 'Driver 1', 'Driver 2', 'Circuit'])
        # Filter the DataFrame by selected circuit using .loc
        filtered_df = df[df['Circuit'] == circuit]
        st.dataframe(df, use_container_width=True, hide_index=True)



    # --- Load data ---
    df = pd.read_excel('F1_data.xlsm', sheet_name='Results', index_col=0)
    df = df.T
    cumulative_points = df.cumsum()
    # --- Plot cumulative points ---
    with st.container(border=True):

        plot_cumulative_points(cumulative_points)

    return database

# Run the app
if __name__ == "__main__":
    main()
