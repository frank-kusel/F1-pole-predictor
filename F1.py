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

page_title = ":red[F1] - 10th Place Cup"
page_icon = ':racing_car:'
layout = 'centered'
# ------------------------------------------------------

# TODO: Add race results input table for admin
# TODO: Create stats for total users, races, guesses etc
# TODO: link constructor to each driver. Show some stats on popular constructors

# --- MAIN APP ---
def main():
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout, menu_items={'Report a Bug': 'mailto:frankuse1@gmail.com'})   
    
    # Page info
    st.title(page_title + " " + page_icon)
    
   
    with st.expander("Menu"):
        st.page_link("pages/Driver Picks.py", label="Driver Picks", icon="🏇")
        st.page_link("pages/Races.py", label="Races", icon="🏎️")
        st.page_link("pages/Stats.py", label="Stats", icon="🧐")
        st.page_link("pages/Welcome.py", label="Welcome", icon="😃")


        
    # Connect to database
    # conn = st.connection("supabase", type=SupabaseConnection)
    # conn = st.connection("postgresql", type="sql")
    conn = db.connect_to_postgresql()
    db.update_points_in_user_guesses(conn)
    

    if conn is None:
        print("Error: Unable to establish database connection.")
        
    
    # driver_names = erg.drivers()
    # st.dataframe(driver_names)
    driver_names = ("Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Zhou Guanyu", "Oscar Piastri", "Sergio Perez", "Charles Leclerc", "Daniel Ricciardo", "Oliver Bearman", "Pierre Gasly", "Fernando Alonso", "Esteban Ocon", "Lance Stroll", "Yuki Tsunoda", "George Russell", "Alex Albon", "Logan Sargeant", "Kevin Magnussen", "Nico Hulkenberg")

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
        with st.expander("Login"):
            
            st.markdown("Login to vote!")
            st.caption("Log in with your existing profile to save your points! Need a password reset? Just send a '🔑' via the WhatsApp group. Default password is 'password'. ")
            
            option = st.radio("", ("Login", "Register"))
              
            with st.form("Login"):

                # Login
            
                if user_id is None: # If user_id is not in session state, perform login

                    if option == "Login":
                        # Login
                        username = st.text_input("Username:", key='username')
                        # st.session_state['username'] = username
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
                        # Registration
                        logged_in = False
                        st.session_state['logged_in'] = logged_in
                        new_username = st.text_input("New Username:")
                        new_password = st.text_input("New Key (password):")
                        
                        if st.form_submit_button("Register"):
                            if db.is_username_taken(conn, (new_username,)):
                                st.warning("Username already taken. Please choose another one.")
                            else:
                                user_id = db.register_user(conn, new_username, new_password)
                                st.success("Registration successful! Please login with your username and password")

    
    with st.container(border=False):
        next_race_date_formatted = next_race_date.strftime('%d %B')
        # next_race_date_formatted = next_race_date

        st.info(f'#### :red[{next_race}] :grey[Grand Prix ] {next_race_date_formatted}')
        st.image('circuit_ID_2.png', output_format="PNG")

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
        sorted_guesses_data = guesses_data.sort_values(by='submission_time', ascending=False)
        # Apply the style to the DataFrame
        
        cmap = mcolors.LinearSegmentedColormap.from_list("", ["#0E1117", "dodgerblue"])
        sorted_guesses_data = (
            sorted_guesses_data.style
            .background_gradient(subset=['points'], cmap=cmap)
            .format({'points': '{:.1f}'})
        )


        # Display DataFrame
        st.caption('Your previous picks...')

        
        st.dataframe(sorted_guesses_data,
                        column_order=( "race_name", "points", "driver_1", "driver_2", "submission_time"), 
                        column_config={
                            "race_name": "Grand Prix",
                            "points": "Points",
                            "driver_1": "Driver 1",
                            "driver_2": "Driver 2",
                            "submission_time": "Submitted"
                        },
                        hide_index=True, 
                        use_container_width=True)


    
    
    
    # --- Leaderboard ---
    
    st.subheader('Leaderboard')
    
    selected_year = st.selectbox("Select year", [2024, 2023])
    leaderboard_df = generate_leaderboard(conn, selected_year)
    
    # Add a bar column based on points
    max_points = leaderboard_df['Points'].max()
    leaderboard_df['Bar'] = leaderboard_df['Points'].apply(lambda x: '|' * int((x / max_points) * 20))
    
    # Round the 'Points' column to one decimal place
    leaderboard_df['Points'] = leaderboard_df['Points'].round(1)
    
    # Display the DataFrame with formatted points
    # Define custom colormap from green to black
    # cmap = mcolors.LinearSegmentedColormap.from_list("", ["#0E1117", "green"]) 
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["#0E1117", "green"]) 
    # Apply styling, including background gradient and position highlights
    styled_leaderboard = leaderboard_df.style \
        .background_gradient(subset=['Points'], cmap=cmap) \
        .format({'Points': '{:.1f}'}) \
        .set_table_styles([{'selector': '.row_heading', 'props': [('text-align', 'left')]}]) \
        .applymap(highlight_positions, subset=pd.IndexSlice[:, 'Position'])

    
    if logged_in: 

            
            # Metrics
            # with st.container(border=False):
            user_name = st.session_state['user_name']
            # Determine the position of the current username in the leaderboard
            # username = st.session_state.get('username')
            current_position = leaderboard_df[leaderboard_df['Name'] == user_name]['Position'].values
            current_points = leaderboard_df[leaderboard_df['Name'] == user_name]['Points'].values
            
            message = st.chat_message("🏆")
            message.write(f':grey[#] :red[{ current_position[0]}] - :grey[{user_name}] - :red[{current_points[0]}] :grey[points]')

                # st.metric(label="Position", value=current_position, delta="-")
                # st.metric(label="Points", value=current_points)
                # current_points.container(height=120).metric("Race Points", points, 0)
                # current_position.container(height=120).metric("Current Position", 10, -5)
                # total_points.container(height=120).metric("Total Points", 98, 12)
                # leader_points.container(height=120).metric("Leader Points", 125, 25)
        
    
    # Display the styled DataFrame
    st.dataframe(styled_leaderboard, use_container_width=True, hide_index=True)
    
    with st.container(border=True):
        st.markdown(f'### :red[2024] Season')
        st.caption('coming soon...')
    
    # --- Load data ---
    with st.container(border=True):
        df = pd.read_excel('F1_data.xlsx', sheet_name='Results', index_col=0)
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
        SELECT u.username, SUM(ug.points) AS total_points
        FROM user_guesses AS ug
        INNER JOIN users AS u ON ug.user_id = u.user_id
        WHERE EXTRACT(YEAR FROM ug.submission_time) = %s
        GROUP BY ug.user_id, u.username
    """
    
    # Execute the query with the year parameter and fetch the results into a DataFrame
    user_points_df = pd.read_sql_query(query, _conn, params=(year,))
    
    # Add a 'Position' column based on the points
    user_points_df['Position'] = user_points_df['total_points'].rank(ascending=False, method='dense').astype(int)
    
    # Select only the required columns 'Name' and 'Points', and order by 'Points' descending
    leaderboard_df = user_points_df[['Position', 'username', 'total_points']].sort_values(by='total_points', ascending=False)
    
    # Rename the columns for clarity
    leaderboard_df.rename(columns={'username': 'Name', 'total_points': 'Points'}, inplace=True)
    
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

# Run the app
if __name__ == "__main__":
    main()
