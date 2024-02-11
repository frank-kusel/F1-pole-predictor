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
import functions.ergast as erg
import plotly.express as px

# ---------------------- SETTINGS ----------------------
race_results = []
page_title = "F1 Pole Predictor"
page_icon = ':racing_car:'
layout = 'centered'
# ------------------------------------------------------

# TODO: Link these lists to the ERGAST API - or just update manually
# TODO: Set the month automatically for each race - user won't need to select circuit

# --- MAIN APP ---
def main():
    
    
    # Page info
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_title + " " + page_icon)
    
    # Menu
    col1, col2 = st.columns(2)
    
    col1.page_link("pages/Pole Picker.py", label="Pole Picker")
    col2.page_link("pages/Race Results.py", label="Race Results")
    
    # Select database
    database = r"f1.db"
    conn = db.create_connection(database)
    
    driver_names = ("Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Zhou Guanyu", "Oscar Piastri", "Sergio Perez", "Charles Leclerc", "Daniel Ricciardo", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso", "Esteban Ocon", "Sebastian Vettel", "Lance Stroll", "Yuki Tsunoda", "George Russell", "Alex Albon", "Logan Sergeant", "Kevin Magnussen", "Nico Hulkenberg")
    # circuit_names = ("Bahrain International Circuit", "Jeddah Street Circuit", "Albert Park Circuit", "Suzuka Circuit", "Shanghai International Circuit", "Hard Rock Stadium Circuit", "Autodromo Enzo e Dino Ferrari", "Circuit de Monaco", "Circuit Gilles Villeneuve", "Circuit de Barcelona-Catalunya", "Red Bull Ring", "Silverstone Circuit", "Hungaroring", "Circuit de Spa-Francorchamps", "Circuit Zandvoort", "Autodromo Nazionale di Monza", "Baku City Circuit", "Marina Bay Street Circuit", "Circuit of the Americas", "Autódromo Hermanos Rodríguez", "Autódromo José Carlos Pace", "Las Vegas Strip Circuit", "Losail International Circuit", "Yas Marina Circuit")

    race_schedule = erg.race_schedule(2024)
    race_schedule_df = pd.DataFrame(race_schedule)
    # Create a new column in the DataFrame that concatenates the race name and date
    race_schedule_df['race_with_date'] = race_schedule_df['raceName'] + ' - ' + pd.to_datetime(race_schedule_df['date']).dt.strftime('%d %B')
    # race_schedule_df['race_with_date'] = race_schedule_df['raceName'] + ' (' + race_schedule_df['date'] + ')'
    # circuit_names = [race['raceName'] for race in race_schedule]
    # circuit_dates = [date['date'] for date in race_schedule]

    # Registration or Login selection
    option = st.radio("Select Option:", ("Login", "Register"), key="register_or_login")
    
    # Retrieve user_id from session state
    user_id = st.session_state.get('user_id')
    logged_in = st.session_state.get('logged_in')
    
    # Login
    if user_id is None: # If user_id is not in session state, perform login

        if option == "Login":
            # Login
            username = st.text_input("Username:")
            password = st.text_input("Password:", type="password")
            logged_in = False
            
            if st.button("Login"):
                user_id = db.authenticate_user(conn, (username, password))
                if not user_id == None:
                    st.success("Login successful!")
                    logged_in=True
                    st.session_state['logged_in'] = logged_in
                    st.session_state['user_id'] = user_id
                else:
                    st.error("Invalid username or password.")
                    logged_in=False
                    
        elif option == "Register":
            # Registration
            logged_in = False
            st.session_state['logged_in'] = logged_in
            new_username = st.text_input("Enter new username:")
            new_password = st.text_input("Enter new password:", type="password")
            
            if st.button("Register"):
                if db.is_username_taken(conn, (new_username,)):
                    st.warning("Username already taken. Please choose another one.")
                else:
                    user_id = db.register_user(conn, (new_username, new_password))
                    st.success("Registration successful!")
        

    if logged_in:
        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                driver1 = st.selectbox(f':green[First] Pick:', sorted(driver_names), key="driver1")
            with col2:
                driver2 = st.selectbox(f':orange[Second] Pick:', sorted(driver_names), key="driver2")
                    
            selected_race_with_date = st.selectbox("Select Race:", race_schedule_df['race_with_date'], key="circuit")  
            circuit = selected_race_with_date.split(' - ')[0]
              
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
        filtered_df = df[df['Name'] == user_id]
        
        # Select only the desired columns
        filtered_df['Points'] = 0
        filtered_df = filtered_df[['Circuit', 'Driver 1', 'Driver 2','Points']]
        
        st.markdown('Your past picks...')
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)



    # --- Load data ---
    
    df = pd.read_excel('F1_data.xlsm', sheet_name='Results', index_col=0)
    df = df.T
    cumulative_points = df.cumsum()
    # --- Plot cumulative points ---
    with st.container(border=False):
        st.markdown(f'### :red[2023] Season')
        st.markdown(f'Winner: **:green[Markus]**')
        plot_cumulative_points(cumulative_points)


    # --- Plot a map ---
    data = [
    {"lon": 50.512, "lat": 26.031, "zoom": 15, "location": "Sakhir", "name": "Bahrain International Circuit", "id": "bh-2002"},
    {"lon": 39.104, "lat": 21.632, "zoom": 14, "location": "Jeddah", "name": "Jeddah Corniche Circuit", "id": "sa-2021"},
    {"lon": 144.970, "lat": -37.846, "zoom": 14, "location": "Melbourne", "name": "Albert Park Circuit", "id": "au-1953"},
    {"lon": 136.534, "lat": 34.844, "zoom": 15, "location": "Suzuka", "name": "Suzuka International Racing Course", "id": "jp-1962"},
    {"lon": 121.221, "lat": 31.340, "zoom": 14, "location": "Shanghai", "name": "Shanghai International Circuit", "id": "cn-2004"},
    {"lon": -80.239, "lat": 25.958, "zoom": 15, "location": "Miami", "name": "Miami International Autodrome", "id": "us-2022"},
    {"lon": 11.713, "lat": 44.341, "zoom": 15, "location": "Imola", "name": "Autodromo Enzo e Dino Ferrari", "id": "it-1953"},
    {"lon": 7.429, "lat": 43.737, "zoom": 15, "location": "Monaco", "name": "Circuit de Monaco", "id": "mc-1929"},
    {"lon": -73.525, "lat": 45.506, "zoom": 14, "location": "Montreal", "name": "Circuit Gilles-Villeneuve", "id": "ca-1978"},
    {"lon": 2.259, "lat": 41.569, "zoom": 14, "location": "Barcelona", "name": "Circuit de Barcelona-Catalunya", "id": "es-1991"},
    {"lon": 14.761, "lat": 47.223, "zoom": 15, "location": "Spielberg", "name": "Red Bull Ring", "id": "at-1969"},
    {"lon": -1.017, "lat": 52.072, "zoom": 14, "location": "Silverstone", "name": "Silverstone Circuit", "id": "gb-1948"},
    {"lon": 19.250, "lat": 47.583, "zoom": 14, "location": "Budapest", "name": "Hungaroring", "id": "hu-1986"},
    {"lon": 5.971, "lat": 50.436, "zoom": 13, "location": "Spa Francorchamps", "name": "Circuit de Spa-Francorchamps", "id": "be-1925"},
    {"lon": 4.541, "lat": 52.389, "zoom": 15, "location": "Zandvoort", "name": "Circuit Zandvoort", "id": "nl-1948"},
    {"lon": 9.290, "lat": 45.621, "zoom": 13, "location": "Monza", "name": "Autodromo Nazionale Monza", "id": "it-1922"},
    {"lon": 49.842, "lat": 40.369, "zoom": 14, "location": "Baku", "name": "Baku City Circuit", "id": "az-2016"},
    {"lon": 103.859, "lat": 1.291, "zoom": 15, "location": "Singapore", "name": "Marina Bay Street Circuit", "id": "sg-2008"},
    {"lon": -97.633, "lat": 30.135, "zoom": 15, "location": "Austin", "name": "Circuit of the Americas", "id": "us-2012"},
    {"lon": -99.091, "lat": 19.402, "zoom": 15, "location": "Mexico City", "name": "Autódromo Hermanos Rodríguez", "id": "mx-1962"},
    {"lon": -46.698, "lat": -23.702, "zoom": 15, "location": "Sao Paulo", "name": "Autódromo José Carlos Pace - Interlagos", "id": "br-1940"},
    {"lon": -115.168, "lat": 36.116, "zoom": 14, "location": "Las Vegas", "name": "Las Vegas Street Circuit", "id": "us-2023"},
    {"lon": 51.454, "lat": 25.49, "zoom": 15, "location": "Lusail", "name": "Losail International Circuit", "id": "qa-2004"},
    {"lon": 54.601, "lat": 24.471, "zoom": 14, "location": "Yas Marina", "name": "Yas Marina Circuit", "id": "ae-2009"}
    ]

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data)

    # Create a scatter plot using Plotly
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="name",
                            zoom=1, height=600, color_discrete_sequence=['red'])

    # Update map layout
    fig.update_layout(mapbox_style="carto-darkmatter")  # Dark map style
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Hide latitude and longitude info when hovering
    fig.update_traces(hovertemplate="<b>%{hovertext}</b>")

    # Display the map in Streamlit
    st.plotly_chart(fig, config ={'displayModeBar': False}, use_container_width=True)


# Run the app
if __name__ == "__main__":
    main()
