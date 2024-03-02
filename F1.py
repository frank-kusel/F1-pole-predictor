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
# import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime
import functions.plot as plot
import functions.database as db
import functions.ergast as erg
# import functions.calculate_points as calc_points

# ---------------------- SETTINGS ----------------------

page_title = "F1 - 10th Place Cup"
page_icon = ':racing_car:'
layout = 'centered'
# ------------------------------------------------------

# TODO: Disable button if user has already submitted a guess for next_race
# TODO: Add race results input table for admin
# TODO: Show race results
# TODO: Create stats for total users, races, guesses etc


# --- MAIN APP ---
def main():
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)   
    print("I ran again")
    # Page info
    st.title(page_title + " " + page_icon)
    if st.button("Driver Picks"):
        st.switch_page("pages/Driver Picks.py") 
        
    # Connect to database
    # conn = st.connection("supabase", type=SupabaseConnection)
    # conn = st.connection("postgresql", type="sql")
    conn = db.connect_to_postgresql()

    if conn is None:
        print("Error: Unable to establish database connection.")
        
    # driver_names = erg.drivers()
    driver_names = ("Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Zhou Guanyu", "Oscar Piastri", "Sergio Perez", "Charles Leclerc", "Daniel Ricciardo", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso", "Esteban Ocon", "Lance Stroll", "Yuki Tsunoda", "George Russell", "Alex Albon", "Logan Sargeant", "Kevin Magnussen", "Nico Hulkenberg")
    
    # race_schedule = erg.race_schedule(2024)
    race_schedule = [
            {'raceName': 'Bahrain', 'date': '2024-03-02', 'circuitName': 'Bahrain International Circuit'},
            {'raceName': 'Saudi Arabian', 'date': '2024-03-09', 'circuitName': 'Jeddah Corniche Circuit'},
            {'raceName': 'Australian', 'date': '2024-03-24', 'circuitName': 'Albert Park Circuit'},
            {'raceName': 'Japanese', 'date': '2024-04-07', 'circuitName': 'Suzuka Circuit'},
            {'raceName': 'Chinese', 'date': '2024-04-21', 'circuitName': 'Shanghai International Circuit'},
            {'raceName': 'Miami', 'date': '2024-05-05', 'circuitName': 'Miami International Autodrome'},
            {'raceName': 'Emilia Romagna', 'date': '2024-05-19', 'circuitName': 'Autodromo Enzo e Dino Ferrari'},
            {'raceName': 'Monaco', 'date': '2024-05-26', 'circuitName': 'Circuit de Monaco'},
            {'raceName': 'Canadian', 'date': '2024-06-09', 'circuitName': 'Circuit Gilles Villeneuve'},
            {'raceName': 'Spanish', 'date': '2024-06-23', 'circuitName': 'Circuit de Barcelona-Catalunya'},
            {'raceName': 'Austrian', 'date': '2024-06-30', 'circuitName': 'Red Bull Ring'},
            {'raceName': 'British', 'date': '2024-07-07', 'circuitName': 'Silverstone Circuit'},
            {'raceName': 'Hungarian', 'date': '2024-07-21', 'circuitName': 'Hungaroring'},
            {'raceName': 'Belgian', 'date': '2024-07-28', 'circuitName': 'Circuit de Spa-Francorchamps'},
            {'raceName': 'Dutch', 'date': '2024-08-25', 'circuitName': 'Circuit Park Zandvoort'},
            {'raceName': 'Italian', 'date': '2024-09-01', 'circuitName': 'Autodromo Nazionale di Monza'},
            {'raceName': 'Azerbaijan', 'date': '2024-09-15', 'circuitName': 'Baku City Circuit'},
            {'raceName': 'Singapore', 'date': '2024-09-22', 'circuitName': 'Marina Bay Street Circuit'},
            {'raceName': 'United States', 'date': '2024-10-20', 'circuitName': 'Circuit of the Americas'},
            {'raceName': 'Mexico City', 'date': '2024-10-27', 'circuitName': 'Autódromo Hermanos Rodríguez'},
            {'raceName': 'São Paulo', 'date': '2024-11-03', 'circuitName': 'Autódromo José Carlos Pace'},
            {'raceName': 'Las Vegas', 'date': '2024-11-23', 'circuitName': 'Las Vegas Strip Street Circuit'},
            {'raceName': 'Qatar', 'date': '2024-12-01', 'circuitName': 'Losail International Circuit'},
            {'raceName': 'Abu Dhabi', 'date': '2024-12-08', 'circuitName': 'Yas Marina Circuit'}
            ]
    race_schedule_df = pd.DataFrame(race_schedule)
    race_schedule_df['race_with_date'] = race_schedule_df['raceName'] + ' - ' + pd.to_datetime(race_schedule_df['date']).dt.strftime('%d %B')
    next_race, next_race_date, circuit_name = erg.next_race_name(race_schedule)
    
    # Retrieve user_id from session state
    user_id = st.session_state.get('user_id')
    logged_in = st.session_state.get('logged_in')
    username = st.session_state.get('username')

    
    
    if not logged_in:
    # with st.expander('Login'):
        # Registration or Login selection
        option = st.radio("Select Option:", ("Login", "Register"))  
        with st.form("Login"):

            # Login
        
            if user_id is None: # If user_id is not in session state, perform login

                if option == "Login":
                    # Login
                    username = st.text_input("Username:", key='username')
                    # st.session_state['username'] = username
                    password = st.text_input("Key:")

                    st.session_state['logged_in'] = False
                    st.session_state['user_id'] = user_id
                    
                    if st.form_submit_button("Login"):
                        user_id = db.authenticate_user(conn, username, password)
                        if user_id > 0:
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
                    new_username = st.text_input("New Username:")
                    new_password = st.text_input("New Key:")
                    
                    if st.form_submit_button("Register"):
                        if db.is_username_taken(conn, (new_username,)):
                            st.warning("Username already taken. Please choose another one.")
                        else:
                            user_id = db.register_user(conn, new_username, new_password)
                            st.success("Registration successful! Please login with your username and password")
    
    
    with st.container(border=False):
        next_race_date_formatted = next_race_date.strftime('%d %B')
        # next_race_date_formatted = next_race_date
        st.info(f'#### :red[{next_race}] Grand Prix - {next_race_date_formatted}')

    if logged_in:
        
        # Fetch circuit ID
        circuit_id = fetch_circuit_id(conn, next_race)

        # Initialize session state
        if "disabled" not in st.session_state:
            st.session_state.disabled = False
        
        # disabled_state = st.session_state.get("disabled", False)
        
        with st.form("entry_form", clear_on_submit=True):

            # st.markdown(f'Hi :blue[{username}], welcome to {circuit_name}')  
            st.markdown(f'Welcome to {circuit_name}') 
            
            col1, col2 = st.columns(2)
            with col1:
                driver_1 = st.selectbox(f':green[First] Pick:', sorted(driver_names), key="driver_1")
            with col2:
                driver_2 = st.selectbox(f':orange[Second] Pick:', sorted(driver_names), key="driver_2")
            
            # if db.save_user_guesses(conn, current_user, driver_1, driver_2, int(circuit_id), submitted_time):
            #     st.error('You have already guessed for this race!') 
                
            submitted = st.form_submit_button(f"__Submit__ :grey[- {next_race}] :grey[Grand Prix]", on_click=disable, disabled=st.session_state.disabled)

            # Save user guesses to a dataframe -> SQLite
            if submitted:
                st.session_state.disabled = True
                submitted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                current_user = st.session_state['user_id']
                
                db.save_user_guesses(conn, current_user, driver_1, driver_2, int(circuit_id), submitted_time)
                st.write(f'You have selected :green[{driver_1}] and :orange[{driver_2}]')
                
        
        
    # Rules
    with st.sidebar:
        with st.expander("Change key"):
            with st.form("Change key", clear_on_submit=True, border=False):
                user = st.text_input("Username:", key='user')
                current_password = st.text_input("Current password:", key='current_password')
                new_password = st.text_input("New password:", key='new_password')
                submitted_new_pw = st.form_submit_button(f"Change password")
                
                if submitted_new_pw:
                    if db.change_password(conn, user, current_password, new_password):
                        st.success("Password updated. You can login with your new password")
                    else:
                        st.error("Error")
        
        with st.container():
            # with st.expander("Racing Rules"):
            st.markdown('#### Racing Rules')
            st.markdown('_Welcome to the F1 - 10th Place Cup! Predict the 10th place driver and earn points._')
            st.markdown('Your first pick earns you the full points, and the second pick gets you half points. Whichever driver gives you the highest score will be used to calculate your points.')
            st.markdown('Driver picks must be submitted 1 hour before the race starts!')
            points_system = {
                "Position": ["10th", "11th", "9th", "12th", "8th", "13th", "7th", "14th", "6th", "15th"],
                "Points": [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
            }
            # df_points_system = pd.DataFrame(points_system)
            st.table(points_system)
    
    
    if logged_in:   
        
        # Fetch user guesses with race names directly from SQL
        guesses_data = pd.DataFrame(fetch_user_guesses(conn, user_id))
        # guesses_data.drop(columns=['guess_id'], inplace=True)

        # # Sort the DataFrame by 'submission_time' column in descending order
        # guesses_data = guesses_data.sort_values(by='submission_time', ascending=False)

        # Display DataFrame
        st.caption('Your previous picks...')
        st.dataframe(guesses_data,
                        column_order=("submission_time", "race_name", "driver_1", "driver_2"), 
                        column_config={
                            "submission_time": "Submitted",
                            "race_name": "Grand Prix",
                            "driver_1": "Driver 1",
                            "driver_2": "Driver 2"
                        },
                        hide_index=True, 
                        use_container_width=True)

    
        #             # Metrics
        # with st.container(border=False):
        #     current_points, current_position, total_points, leader_points = st.columns(4)
            
        #     points = calc_points.points(user_id, driver_1, driver_2)
            
        #     current_points.container(height=120).metric("Race Points", points, 0)
        #     current_position.container(height=120).metric("Current Position", 10, -5)
        #     total_points.container(height=120).metric("Total Points", 98, 12)
        #     leader_points.container(height=120).metric("Leader Points", 125, 25)
    
    
    # --- Leaderboard ---
    
    st.subheader('Leaderboard')
    # Read the Excel file into a DataFrame
    df = pd.read_excel('temp_results.xlsm', sheet_name='Points')

    # Add a 'Position' column based on the points
    df['Position'] = df['Points'].rank(ascending=False, method='dense').astype(int)
    
    # Select only the required columns 'Name' and 'Points', and order by 'Points' descending
    df_sorted = df[['Position', 'Name', 'Points']].sort_values(by='Points', ascending=False)
    
    
    # Reset the index to have consecutive integer index starting from 1
    df_sorted.reset_index(drop=True, inplace=True)
    
    # Add a bar column based on points
    max_points = df_sorted['Points'].max()
    df_sorted['Bar'] = df_sorted['Points'].apply(lambda x: '|' * int((x / max_points) * 20))
    
    # Round the 'Points' column to one decimal place
    df_sorted['Points'] = df_sorted['Points'].round(1)
    
    # Display the DataFrame with formatted points
    # Define custom colormap from green to black
    # cmap = mcolors.LinearSegmentedColormap.from_list("", ["#0E1117", "green"]) 
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["#0E1117", "darkgreen"]) 
    st.dataframe(df_sorted.style.background_gradient(subset=['Points'], cmap=cmap), use_container_width=True, hide_index=True)
    

    # Display the styled DataFrame with a bar chart representation for the 'Points' column
    # styled_df = df_sorted.style.bar(subset=['Points'], color='green')

    
    with st.container(border=True):
        st.markdown(f'### :red[2024] Season')
        st.caption('coming soon...')
        

    
    # --- Load data ---
    with st.container(border=True):
        df = pd.read_excel('F1_data.xlsm', sheet_name='Results', index_col=0)
        df = df.T
        cumulative_points = df.cumsum()
        # --- Plot cumulative points ---
        with st.container(border=False):
            st.markdown(f'### :red[2023] Season')
            plot.plot_cumulative_points(cumulative_points)


    # --- Plot a map ---
    with st.container(border=True):
        plot.map_locations()

def disable():
    st.session_state.disabled = True


@st.cache_data
def fetch_circuit_id(_conn, race_name):
    """
    Fetch the circuit ID for a given race name.
    """
    query = '''
            SELECT circuit_id FROM race_info WHERE race_name = %s
            '''
    with _conn.cursor() as cursor:
        cursor.execute(query, (race_name,))
        circuit_id = cursor.fetchone()[0]
    return circuit_id


# @st.cache_data
def fetch_user_guesses(_conn, user_id):
    """
    Fetch user guesses with race names directly from SQL.
    """
    query = '''
            SELECT
                ug.guess_id,
                rd.race_name, 
                ug.driver_1, 
                ug.driver_2,
                ug.submission_time 
            FROM
                user_guesses ug
            JOIN 
                race_info rd ON ug.circuit_id = rd.circuit_id
            JOIN
                users ON ug.user_id = users.user_id
            WHERE 
                ug.user_id = %s
            '''
    with _conn.cursor() as cursor:
        cursor.execute(query, (user_id,))
        columns = [desc[0] for desc in cursor.description]
        guesses_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return guesses_data

# Run the app
if __name__ == "__main__":
    main()
