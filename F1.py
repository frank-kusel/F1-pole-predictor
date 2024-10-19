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
import matplotlib.colors as mcolors
import functions.plot as plot
import functions.database as db
import functions.ergast as erg
from datetime import datetime
# import fastf1.plotting
import numpy as np
# import fastf1
import plotly.graph_objects as go

# TODO: Create stats for total users, races, guesses etc
# TODO: link constructor to each driver. Show some stats on popular constructors

# ---------------------- SETTINGS ----------------------
page_title = ":red[F1]   10th Place Cup"
page_icon = ':racing_car:'
layout = 'centered'
# ------------------------------------------------------

# Main function
def main():
    # Page info
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout,
                        menu_items={'Report a Bug': 'mailto:frankuse1@gmail.com'})
    # Navigation menu
    with st.popover("Menu"):
        st.page_link("pages/Driver Picks.py", label="Driver Picks", icon="🏇")
        st.page_link("pages/Races.py", label="Races", icon="🏎️")
        st.page_link("pages/Stats.py", label="Stats", icon="🧐")
        st.page_link("pages/Welcome.py", label="Welcome", icon="😃")

    st.title(f"{page_title}")
    

    # Database connection
    conn = db.connect_to_postgresql()
    
    if conn is None:
        print("Error: Unable to establish database connection.")
        
    # Fetch drivers, race_schedule, next_race, next_race_date, circuit_name
    # race_schedule = erg.race_schedule(2024)
    # driver_names = erg.drivers()
    # if driver_names is None:
    
    
    driver_names = ("Lewis Hamilton","Kevin Magnussen", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Zhou Guanyu", "Oscar Piastri", "Sergio Pérez", "Charles Leclerc", "Liam Lawson", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso", "Esteban Ocon", "Lance Stroll", "Yuki Tsunoda", "George Russell", "Alexander Albon", "Franco Colapinto", "Nico Hülkenberg")
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
        
    next_race, next_race_date, circuit_name = erg.next_race_name(race_schedule)
    st.session_state['next_race_date'] = next_race_date
    # Retrieve user_id from session state
    user_id = st.session_state.get('user_id')
    logged_in = st.session_state.get('logged_in')
    username = st.session_state.get('username')
    
    # If not logged in, show login form
    if not logged_in:
        with st.expander("👉Login to Vote"):
            st.markdown("Login to vote!")
            st.caption("Log in with your existing profile to save your points! Need a password reset? Just send a '🔑' via the WhatsApp group. Default password is 'password'. ")
            option = st.radio("", ("Login", "Register"))
                
            with st.form("Login"):
                if option == "Login":
                    username = st.text_input("Username:", key='username')
                    password = st.text_input("Key (password):")
                    st.session_state['logged_in'] = False
                    st.session_state['user_id'] = user_id
                    user_name = st.session_state['user_name'] = username
                    
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
                    st.session_state['logged_in'] = logged_in = False
                    new_username = st.text_input("New Username:")
                    new_password = st.text_input("New Key (password):")
                    
                    if st.form_submit_button("Register"):
                        if db.is_username_taken(conn, (new_username,)):
                            st.warning("Username already taken. Please choose another one.")
                        else:
                            user_id = db.register_user(conn, new_username, new_password)
                            st.success("Registration successful! Please login with your username and password")

    # Next race info and circuit map
    with st.container(border=False):
        
        next_race_date_formatted = next_race_date.strftime('%d %B')
        
        # Calculate the number of days until the next race date
        days_until_race = (next_race_date - datetime.now().date()).days
        
        # st.error(f'#### :red[{next_race}] :grey[Grand Prix ] {next_race_date_formatted}')
        st.error(f'#### {next_race} :grey[Grand Prix ] {next_race_date_formatted}')
        st.caption(f"Days until race: :red[{days_until_race}]")
        
        # map = st.selectbox('Select Circuit', ['Abudhabi', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Belgium', 'Brazil', 'Canada', 'China', 'France', 'Greatbritain', 'Hungary', 'Italy', 'Japan', 'Mexico', 'Monaco', 'Netherlands', 'Russia', 'Singapore', 'Spain', 'Usa', 'Vietnam'])
        
        map = next_race
        track_maps_folder = 'track_maps/'
        extensions = ['.svg', '.png']
        
        # Initialize map_image as None
        map_image = None

        # Loop through extensions to find the map file
        for ext in extensions:
            map_image_path = f'{track_maps_folder}{map}{ext}'
            try:
                with open(map_image_path):
                    map_image = map_image_path
                    break
            except FileNotFoundError:
                continue

        if map_image:
            # Display the image
            st.image(map_image, caption=f'{circuit_name}', use_column_width=True)
        else:
            st.error(f'Map image for {map} not found.')
       
        
        
    # If logged in, show personal stats
    if logged_in:
        circuit_id = fetch_circuit_id(conn, next_race)

        # Initialize session state for the form_submit_button
        if "disabled" not in st.session_state:
            st.session_state.disabled = False
        
        with st.form("entry_form"):
            col1, col2 = st.columns(2)
            with col1:
                driver_1 = st.selectbox(f':red[Driver 1]', sorted(driver_names), key="driver_1")
            with col2:
                driver_2 = st.selectbox(f':grey[Driver 2]', sorted(driver_names), key="driver_2")
            submitted = st.form_submit_button(f":green[Submit] :grey[- {next_race}] :grey[Grand Prix]", on_click=disable, disabled=st.session_state.disabled)

            if submitted:
                st.session_state.disabled = True
                submitted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                current_user = st.session_state['user_id']
                
                db.save_user_guesses(conn, current_user, driver_1, driver_2, int(circuit_id), submitted_time)
                st.write(f'You have selected :green[{driver_1}] and :orange[{driver_2}]')
        
        # Display DataFrame
        st.markdown('##### Your previous picks')
        
        # Fetch user guesses with race names directly from SQL
        guesses_data = pd.DataFrame(fetch_user_guesses(conn, user_id))
        
        latest_submission_time = guesses_data['submission_time'].max()
        st.session_state['latest_submission_time'] = latest_submission_time
        
        sorted_guesses_data = guesses_data.sort_values(by='submission_time', ascending=False)
        # sorted_guesses_data = guesses_data
        # sorted_guesses_data

        cmap = mcolors.LinearSegmentedColormap.from_list("", ["#0E1117", "dodgerblue"])
        sorted_guesses_data = (
            sorted_guesses_data.style
            .background_gradient(subset=['points'], cmap=cmap)
            .format({'points': '{:.1f}'})
        )

        st.dataframe(sorted_guesses_data,
                        column_order=( "race_name", "points", "driver_1", "driver_2", "submission_time"), 
                        column_config={
                            "race_name": "Grand Prix",
                            "points": "Points",
                            "driver_1": "Driver 1",
                            "driver_2": "Driver 2",
                            "submission_time": "Time UTC+00:00"
                        },
                        hide_index=True, 
                        use_container_width=True)        
        
    # Change password in sidebar
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
     
    # --- Leaderboard ---
    st.subheader('Leaderboard')
    
    selected_year = st.selectbox("Select year", [2024, 2023]) 
    
    leaderboard_df = generate_leaderboard(conn, selected_year)
    
    
    # Filter the DataFrame based on the '🤑' column
    filter_options = ['All', 'Premium', 'Non-Premium']
    filter_option = st.selectbox("Filter Leaderboard", filter_options)

    # Apply filtering based on the selected option
    if filter_option == 'Premium':
        leaderboard_df = leaderboard_df[leaderboard_df['Paid'].notnull()]
    elif filter_option == 'Non-Premium':
        leaderboard_df = leaderboard_df[leaderboard_df['Paid'].isnull()]

   
    
    
    query = """
            SELECT
                ri.race_name,
                u.username,
                ri.date,
                ug.submission_time,
                SUM(ug.points) OVER (PARTITION BY u.username ORDER BY ri.date) AS cumulative_points
            FROM
                user_guesses ug
            JOIN
                users u ON ug.user_id = u.user_id
            JOIN
                race_info ri ON ug.circuit_id = ri.circuit_id
            WHERE
                EXTRACT(YEAR FROM ug.submission_time) = 2024
            ORDER BY
                ri.date, u.username;
    """

    with conn.cursor() as cursor:

        # Execute the query and fetch the results
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(data, columns=columns)
        
        # Convert 'date' column to datetime format
        df['date'] = pd.to_datetime(df['date'])

        # Concatenate MM-DD from 'date' with 'race_name'
        df['race_with_date'] = df['date'].dt.strftime('%m-%d') + ' ' + df['race_name']
        
        # Filter the df to exclude the submission_times that are after the prev_race_date
        # TODO: when the race happens, the leaderboard might not update because of this filtration... check what happens here
        prev_race_date = erg.previous_race_date(race_schedule)
        prev_race_date = datetime.combine(prev_race_date, datetime.max.time())


        race_before_prev_race_date = erg.race_before_previous_date(race_schedule)
        race_before_prev_race_date = datetime.combine(race_before_prev_race_date, datetime.max.time())
        

        df = df[df['date'] <= prev_race_date]

        # Drop duplicate rows based on the combined key
        # df_cleaned = df.drop_duplicates(subset='username', keep='last')




        # Combine race_name and username to identify duplicates
        df['key'] = df['race_name'] + '_' + df['username']

        # Drop duplicate rows based on the combined key
        df_cleaned = df.drop_duplicates(subset='key', keep='first')

        # Drop the temporary 'key' column
        df_cleaned = df_cleaned.drop(columns=['key'])






        # Pivot the DataFrame to get the desired format without reordering the index
        pivot_df = df_cleaned.pivot(index='race_with_date', columns='username', values='cumulative_points')
        
        # Fill NaN values with the previous non-null value (forward fill)
        pivot_df.fillna(method='ffill', inplace=True)
        
        # Fill remaining None values with 0
        pivot_df.fillna(0, inplace=True)
        
        # Get the race date of the latest race
        latest_race_date = pivot_df.index[-1]
        
        # Get the race date of the previous race
        prev_race_date_index = pivot_df[pivot_df.index < latest_race_date].index.max()
        prev_race_date = prev_race_date_index if prev_race_date_index is not None else latest_race_date
        
        # Get the previous race positions
        prev_race_positions = pivot_df.loc[prev_race_date]
        
        # Sort the points for the previous race and calculate positions
        prev_race_sorted = prev_race_positions.sort_values()
        prev_race_positions = prev_race_sorted.rank(ascending=False, method='min')
        

        all_users = leaderboard_df['Name']
        
        # Identify users in all_users that are not in prev_race_positions
        new_users = all_users[~all_users.isin(prev_race_positions.index)]

        # Add new users to prev_race_positions with a default position of -1
        for user in new_users:
            prev_race_positions[user] = -1


        # Iterate over each user in the leaderboard dataframe to get the arrow and positions_moved
        
        leaderboard_df['↕️'], leaderboard_df['?'] = zip(*leaderboard_df.apply(lambda row: get_arrow(prev_race_positions[row['Name']], row['Position']), axis=1))    
        
        # Reorder columns from Position, Name, Points, Paid, Bar, Arrow, ? to Position, Paid, Name, Arrow, ?, Points, Bar
        # leaderboard_df = leaderboard_df[['Position', 'Paid', 'Name', '↕️', '?', 'Points']]
        # Rename columns using the rename() method
        leaderboard_df['Paid'] = leaderboard_df['Paid'].replace('paid', '🤑')
        leaderboard_df.rename(columns={'Position': '#', 'Paid': '🤑'}, inplace=True)
        # leaderboard_df = leaderboard_df.rename(columns={'Position': '#'})
        # Reorder columns
        leaderboard_df = leaderboard_df[['#', '↕️', '?', 'Name', 'Points', '🤑']]

        styled_leaderboard = style_leaderboard(leaderboard_df)  
    
    # Metrics
    if logged_in:
            user_name = st.session_state['user_name']
            # Check if the 'Name' column is equal to 'user_name' or 'user_name 🤑'
            current_position = leaderboard_df[(leaderboard_df['Name'] == user_name) | (leaderboard_df['Name'] == f"{user_name} 🤑")]['#'].values
            current_points = leaderboard_df[(leaderboard_df['Name'] == user_name) | (leaderboard_df['Name'] == f"{user_name} 🤑")]['Points'].values

            message = st.chat_message("🏆")
            message.write(f':grey[#] :red[{ current_position[0]}] - :grey[{user_name}] - :red[{current_points[0]}] :grey[points]')   
    
    # Display the styled DataFrame
    # st.caption("🤑 -> premium players")

    st.dataframe(styled_leaderboard, use_container_width=True, hide_index=True)

    
    # 2024 Season
    with st.container(border=False):
        
        # Assuming `cursor` is your database cursor object and `conn` is your database connection object
        query = """
                SELECT
                    ri.race_name,
                    u.username,
                    ri.date,
                    ug.submission_time,
                    SUM(ug.points) OVER (PARTITION BY u.username ORDER BY ri.date) AS cumulative_points
                FROM
                    user_guesses ug
                JOIN
                    users u ON ug.user_id = u.user_id
                JOIN
                    race_info ri ON ug.circuit_id = ri.circuit_id
                WHERE
                    EXTRACT(YEAR FROM ug.submission_time) = 2024
                ORDER BY
                    ri.date, u.username;
        """

        with conn.cursor() as cursor:

            # Execute the query and fetch the results
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            # Create a DataFrame from the fetched data
            df = pd.DataFrame(data, columns=columns)
            
            # Convert 'date' column to datetime format
            df['date'] = pd.to_datetime(df['date'])

            # Concatenate MM-DD from 'date' with 'race_name'
            df['race_with_date'] = df['date'].dt.strftime('%m-%d') + ' ' + df['race_name']

            # Combine race_name and username to identify duplicates
            df['key'] = df['race_name'] + '_' + df['username']

            # Drop duplicate rows based on the combined key
            df_cleaned = df.drop_duplicates(subset='key', keep='first')

            # Drop the temporary 'key' column
            df_cleaned = df_cleaned.drop(columns=['key'])



            # Pivot the DataFrame to get the desired format without reordering the index
            pivot_df = df_cleaned.pivot(index='race_with_date', columns='username', values='cumulative_points')
          
            # Fill NaN values with the previous non-null value (forward fill)
            pivot_df.fillna(method='ffill', inplace=True)
            
            # Fill remaining None values with 0
            pivot_df.fillna(0, inplace=True)
            
            # --- Plot cumulative points ---
            with st.container(border=False):
                st.markdown(f'### :red[2024] Season')
                plot.plot_cumulative_points(pivot_df)
                
    
    # 2023 Season
    with st.container(border=False):
        
        # Assuming `cursor` is your database cursor object and `conn` is your database connection object
        query = """
                SELECT
                    ri.race_name,
                    u.username,
                    ri.date,
                    ug.submission_time,
                    SUM(ug.points) OVER (PARTITION BY u.username ORDER BY ri.date) AS cumulative_points
                FROM
                    user_guesses ug
                JOIN
                    users u ON ug.user_id = u.user_id
                JOIN
                    race_info ri ON ug.circuit_id = ri.circuit_id
                WHERE
                    EXTRACT(YEAR FROM ug.submission_time) = 2023
                ORDER BY
                    ri.date, u.username;
        """

        with conn.cursor() as cursor:

        # Execute the query and fetch the results
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            # Create a DataFrame from the fetched data
            df = pd.DataFrame(data, columns=columns)
            
            # Convert 'date' column to datetime format
            df['date'] = pd.to_datetime(df['date'])

            # Concatenate MM-DD from 'date' with 'race_name'
            df['race_with_date'] = df['date'].dt.strftime('%m-%d') + ' ' + df['race_name']

            # Pivot the DataFrame to get the desired format without reordering the index
            pivot_df2 = df.pivot(index='race_with_date', columns='username', values='cumulative_points')

            # --- Plot cumulative points ---
            with st.container(border=False):
                st.markdown(f'### :red[2023] Season')
                plot.plot_cumulative_points(pivot_df2)
    
    # db.update_points_in_user_guesses(conn)
    
    # --- Plot a map ---
    # with st.container(border=False):
    #     plot.map_locations()

    

def disable():
    st.session_state.disabled = True

# Highlight maximum values in the 'points' column in green
def highlight_max(s):
    is_max = s == s.max()
    return ['color: green' if v else '' for v in is_max]

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

def highlight_positions(val):
    if val in [1, 2, 3]:
        return 'font-weight: bold; color: green'
    if val in [10]:
        return 'font-weight: bold; color: red'
    else:
        return ''

def generate_leaderboard(_conn, year):
    # Query the database to get the total points for each user_id and their username
    query = """
        SELECT u.username, u.premium, SUM(ug.points) AS total_points
        FROM user_guesses AS ug
        INNER JOIN users AS u ON ug.user_id = u.user_id
        WHERE EXTRACT(YEAR FROM ug.submission_time) = %s
        AND ug.points IS NOT NULL
        GROUP BY ug.user_id, u.username, u.premium
    """
    
    # Execute the query with the year parameter and fetch the results into a DataFrame
    user_points_df = pd.read_sql_query(query, _conn, params=(year,))
    
    # Add a 'Position' column based on the points
    user_points_df['Position'] = user_points_df['total_points'].rank(ascending=False, method='min').astype(int)
    
    # Select only the required columns 'Name' and 'Points', and order by 'Points' descending
    leaderboard_df = user_points_df[['Position', 'username', 'total_points', 'premium']].sort_values(by='total_points', ascending=False)

    # Rename the columns for clarity
    leaderboard_df.rename(columns={'username': 'Name', 'total_points': 'Points', 'premium':'Paid'}, inplace=True)
    
     # Check if the 'Premium' column exists in the DataFrame
    if 'premium' in leaderboard_df.columns:
        # Add $ symbol to the name if Premium is not NULL
        # leaderboard_df['Name'] = leaderboard_df.apply(lambda row: f"{row['Name']} 🤑" if row['premium'] is not None else row['Name'], axis=1)
        None
    return leaderboard_df

def generate_prev_leaderboard(_conn, year):
    # Query the database to get the total points for each user_id and their username
    query = """
        SELECT u.username, u.premium, SUM(ug.points) AS total_points
        FROM user_guesses AS ug
        INNER JOIN users AS u ON ug.user_id = u.user_id
        WHERE EXTRACT(YEAR FROM ug.submission_time) = %s
        AND ug.points IS NOT NULL
        AND ug.circuit_id <> (SELECT circuit_id FROM race_info WHERE date = (SELECT MAX(date) FROM race_info))
        GROUP BY ug.user_id, u.username, u.premium
    """
    
    # Execute the query with the year parameter and fetch the results into a DataFrame
    user_points_df = pd.read_sql_query(query, _conn, params=(year,))
    
    # Add a 'Position' column based on the points
    user_points_df['Position'] = user_points_df['total_points'].rank(ascending=False, method='min').astype(int)
    
    # Select only the required columns 'Name' and 'Points', and order by 'Points' descending
    leaderboard_df = user_points_df[['Position', 'username', 'total_points', 'premium']].sort_values(by='total_points', ascending=False)

    # Rename the columns for clarity
    leaderboard_df.rename(columns={'username': 'Name', 'total_points': 'Points', 'premium':'Paid'}, inplace=True)
    
    # Check if the 'Premium' column exists in the DataFrame
    if 'premium' in leaderboard_df.columns:
        # Add $ symbol to the name if Premium is not NULL
        # leaderboard_df['Name'] = leaderboard_df.apply(lambda row: f"{row['Name']} 🤑" if row['premium'] is not None else row['Name'], axis=1)
        None
    
    return leaderboard_df


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
                ug.submission_time, 
                ug.points 
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

def style_leaderboard(leaderboard_df):
    # Add a bar column based on points
    max_points = leaderboard_df['Points'].max()
    leaderboard_df['Bar'] = leaderboard_df['Points'].apply(lambda x: '|' * int((x / max_points) * 20))
    
    # Round the 'Points' column to one decimal place
    leaderboard_df['Points'] = leaderboard_df['Points'].round(1)
    
    # Define custom colormap from green to black
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["#0E1117", "green"]) 
    
    # Drop the 'premium' column
    # leaderboard_df.drop('premium', axis=1, inplace=True)
    
    # Apply styling, including background gradient and position highlights
    styled_leaderboard = leaderboard_df.style \
        .background_gradient(subset=['Points'], cmap=cmap) \
        .format({'Points': '{:.1f}'}) \
        .set_table_styles([{'selector': '.row_heading', 'props': [('text-align', 'left')]}]) \
        .map(highlight_positions, subset=pd.IndexSlice[:, '#'])
    
    return styled_leaderboard

# Function to determine arrow direction
def get_arrow(prev_position, current_position):

    if prev_position == -1:
            return '🌱', '-'


    if prev_position < current_position:
        arrow = '💔'  
        positions_moved = -round(abs(prev_position - current_position))
        return arrow, positions_moved
    elif prev_position > current_position:
        arrow = '💚'  
        positions_moved = +round(abs(prev_position - current_position))
        return arrow, positions_moved
    else:
        arrow = '😶'  
        positions_moved = 0
        return arrow, positions_moved
    

if __name__ == "__main__":
    main()
