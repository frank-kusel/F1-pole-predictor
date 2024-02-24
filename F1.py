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
import functions.plot as plot
import functions.database as db
import functions.ergast as erg
import plotly.express as px
import functions.calculate_points as calc_points
from sqlite3 import Error

# ---------------------- SETTINGS ----------------------
race_results = []
page_title = "F1 Pole Predictor"
page_icon = ':racing_car:'
layout = 'centered'
# ------------------------------------------------------



# TODO: Show race results
# TODO: Create a function that only allows race entries once, and once per current next race
# TODO: Create year filter in pole picker for favourite drivers
# TODO: prevent the app from refetching driver names and race schedules on each click..
# TODO: redo login logic.. or use the empty container function: https://discuss.streamlit.io/t/login-form-using-st-form/26722
# TODO: Create a year filter for each user's past picks
# TODO: Create stats for total users, races, guesses etc


# --- MAIN APP ---
def main():
    
    # Page info
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_title + " " + page_icon)
    
    # Select database
    database = r"F1.db"
    conn = create_connection(database)
    st.write(conn)
    
    
    
    users_df = pd.read_sql('SELECT * from users', conn)
    st.dataframe(users_df, use_container_width=True, hide_index=True)
    st.markdown(authenticate_user(conn,('Frank', 'password')))
    
    
    
    
    if conn is None:
        print("Error: Unable to establish database connection.")
        
    driver_names = erg.drivers()
    # driver_names = ("Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Zhou Guanyu", "Oscar Piastri", "Sergio Perez", "Charles Leclerc", "Daniel Ricciardo", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso", "Esteban Ocon", "Sebastian Vettel", "Lance Stroll", "Yuki Tsunoda", "George Russell", "Alex Albon", "Logan Sergeant", "Kevin Magnussen", "Nico Hulkenberg")
    
    race_schedule = erg.race_schedule(2024)
    race_schedule_df = pd.DataFrame(race_schedule)
    race_schedule_df['race_with_date'] = race_schedule_df['raceName'] + ' - ' + pd.to_datetime(race_schedule_df['date']).dt.strftime('%d %B')
    next_race, next_race_date = erg.next_race_name(race_schedule)
    
    with st.expander('Login'):
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
                    user_id = authenticate_user(conn, (username, password,))
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
                    if is_username_taken(conn, (new_username,)):
                        st.warning("Username already taken. Please choose another one.")
                    else:
                        user_id = register_user(conn, (new_username, new_password))
                        st.success("Registration successful!")
        

    if logged_in:
        
        
        # SQL query to return circuit_id
        curr = conn.cursor()
        curr.execute("SELECT circuit_id FROM race_details WHERE race_name = ? ", (next_race,))
        result = curr.fetchone()
        circuit_id = result[0]
        print(f'circuit id: {circuit_id}')
        
        # Initialize session state
        if "disabled" not in st.session_state:
            st.session_state.disabled = False
        
        with st.form("entry_form", clear_on_submit=True):
            
            next_race_date_formatted = next_race_date.strftime('%d %B')
            st.markdown(f'#### Next race: :red[{next_race}] - {next_race_date_formatted}')
            current_date = datetime.today()
            # Convert the next_race_date to a datetime object
            next_race_datetime = datetime.combine(next_race_date, datetime.min.time())
            time_difference = (next_race_datetime - current_date).days
            st.markdown(f'*Days until next race: {time_difference}*')
            
            col1, col2 = st.columns(2)
            with col1:
                driver_1 = st.selectbox(f':green[First] Pick:', sorted(driver_names), key="driver_1")
            with col2:
                driver_2 = st.selectbox(f':orange[Second] Pick:', sorted(driver_names), key="driver_2")
                    
            submitted = st.form_submit_button("Place your bet!", on_click=disable, disabled=st.session_state.disabled)

            # Save user guesses to a dataframe -> SQLite
            if submitted:
                
                st.session_state.show_submit_button = False
                submitted_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                current_user = st.session_state['user_id']

                
                save_user_guesses(conn, (current_user, driver_1, driver_2, circuit_id, submitted_time))
                st.write(f'You have selected :green[{driver_1}] and :orange[{driver_2}]')
    

    
    
        # Metrics
        with st.container(border=False):
            current_points, current_position, total_points, leader_points = st.columns(4)
            
            points = calc_points.main(user_id, driver_1, driver_2)
            
            current_points.container(height=120).metric("Race Points", points, 0)
            current_position.container(height=120).metric("Current Position", 10, -5)
            total_points.container(height=120).metric("Total Points", 98, 12)
            leader_points.container(height=120).metric("Leader Points", 125, 25)
    
    
        
    # Rules
    with st.sidebar:
        with st.container():
            with st.expander("Racing Rules"):
                st.markdown('_Welcome to the F1 Prediction Game! Predict the 10th place driver and earn points._')
                points_system = {
                    "Position": ["10th", "11th", "9th", "12th", "8th", "13th", "7th", "14th", "6th", "15th", "5th"],
                    "Points": [25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0.5]
                }
                df_points_system = pd.DataFrame(points_system)
                st.dataframe(points_system, hide_index=True, use_container_width=True)
    
    
    if logged_in:   
        
        # Fetch user guesses with race names directly from SQL
        c = conn.cursor()
        c.execute("""
            SELECT ug.submission_time, rd.race_name, ug.driver_1, ug.driver_2
            FROM user_guesses ug
            JOIN race_details rd ON ug.circuit_id = rd.circuit_id
            WHERE ug.user_id = ?
        """, (user_id,))
        guesses_data = c.fetchall()

        # Convert the data to a DataFrame
        filtered_df = pd.DataFrame(guesses_data, columns=['Submitted', 'Race', 'Driver 1', 'Driver 2'])

        # Display DataFrame
        st.markdown('Your previous picks...')
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    
    # --- Load data ---
    
    df = pd.read_excel('F1_data.xlsm', sheet_name='Results', index_col=0)
    df = df.T
    cumulative_points = df.cumsum()
    # --- Plot cumulative points ---
    with st.container(border=False):
        st.markdown(f'### :red[2023] Season')
        st.markdown(f'Winner: **:green[Markus]**')
        plot.plot_cumulative_points(cumulative_points)


    # --- Plot a map ---
    plot.map_locations()


def disable():
    st.session_state.disabled = True
    
# Create a db connection
def create_connection(db_file):
    """Create a databse connection to a SQLite databse specified by a db_file
    :param: db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    
    except Error as e:
        print(e)
        
    return conn

# Create db tables
def create_table(conn, create_table_sql):
    """ create a table from the creat_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Insert data
def register_user(conn, user_details):
    """
    Create a new user into the users table
    :param conn:
    :param user: username and password
    :return: user id
    """
    sql = ''' INSERT INTO users (username, password)
              VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, user_details)
    conn.commit()
    return cur.lastrowid

# Function to save user guesses
def save_user_guesses(conn, user_guesses):
    """
    Insert user guesses into the user_guesses table
    :param conn:
    :param user_guesses: user_id, driver_1, driver_2, circuit
    :return:
    """
    sql = ''' INSERT INTO  user_guesses (user_id, driver_1, driver_2, circuit_id, submission_time)
                VALUES (?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, user_guesses)
    conn.commit()

# Function to check if username already exists
def is_username_taken(conn, username):
    """
    Check whether username already exists
    :param conn:
    :param username:
    :return: True or False
    """
    sql = ''' SELECT * FROM users WHERE username=?'''
    cur = conn.cursor()
    cur.execute(sql, username)
    return cur.fetchone() is not None

# Function to authenticate user
def authenticate_user(conn, login_details):
    """
    Authenticate user
    :param conn:
    :param login_details: username and password
    :return: True or False if user has logged in correctly
    """
    sql = ''' SELECT * FROM users WHERE username=? AND password=?'''
    c = conn.cursor()
    c.execute(sql, login_details)
    user_data = c.fetchone()
    if user_data:
        user_id = int(user_data[0])
        return user_id  # Authentication successful
    else:
        return None  # Authentication failed


# Run the app
if __name__ == "__main__":
    main()
