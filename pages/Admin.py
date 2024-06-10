import streamlit as st
import functions.database as db
import functions.ergast as erg
import pandas as pd
import pages.Races as race

st.title("Admin")

conn = db.connect_to_postgresql()
db.update_points_in_user_guesses(conn)

st.image('admin_mascot.png', use_column_width=True, caption='Stop. Admin only 👀')

# Create admin section
password = 'cakecakecake'

key = st.text_input('Admin:')

# Function to insert race results into the database
def insert_race_results(conn, circuit_id, df_race_results, season):
    try:
        with conn.cursor() as cursor:
            # Delete existing race results for the given season
            cursor.execute("DELETE FROM race_results WHERE season = %s AND circuit_id = %s", (season, circuit_id,))

            # Insert new race results into the database
            for index, row in df_race_results.iterrows():
                # Check if the driver is not NULL before inserting
                if int(row['position']) != 0:
                    st.write(row['position'])
                    cursor.execute(
                        "INSERT INTO race_results (circuit_id, driver, position, season) VALUES (%s, %s, %s, %s)",
                        (circuit_id, row['driver'], row['position'], season)
                    )

        conn.commit()
        st.success("Race results submitted successfully!")
    except Exception as e:
        st.error(f"Error: {e}")
        return


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


def show_users():
    conn = db.connect_to_postgresql()
    sql = "SELECT * FROM users"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        df_users = pd.DataFrame(rows, columns=['user_id', 'username', 'password', 'premium'])
        
    return df_users


if key == password:
    
    conn = db.connect_to_postgresql()
    
    # Show a database of the usernames and passwords from the databse users table
    # st.subheader('Users')
    # st.dataframe(show_users(), hide_index=True)
    
    # Sample list of driver names
    driver_names = erg.drivers()
    
    if driver_names is None:
        driver_names = ("Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Guanyu Zhou", "Oscar Piastri", "Sergio Pérez", "Charles Leclerc", "Daniel Ricciardo", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso", "Esteban Ocon", "Lance Stroll", "Yuki Tsunoda", "George Russell", "Alexander Albon", "Logan Sargeant", "Kevin Magnussen", "Nico Hülkenberg")

    driver_names
    
    # Create a DataFrame to hold the data
    df_race_results = pd.DataFrame({
        'driver': driver_names,
        'position': [None] * len(driver_names)
    })

    race_schedule = erg.race_schedule(2024)
    if race_schedule is None:
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
    
    race_names = [race['raceName'] for race in race_schedule]

    # Display the form with data editor for user input
    
    season = st.selectbox('Season',(2024, 2025))
    selected_race = st.selectbox('Race Name', race_names)
    st.info('Make sure the race and year is correct before submitting. Submitting will overwrite previous race results. *:red[This form uploads and overwrites race results for the selected race and season. Use with caution!]*')
    
    with st.form(key='auto_race_results_form'):
        
        st.subheader(":green[Automatic] Entry")
        st.caption('If official race results are available for the selected race, submit this form to upload results. Otherwise, you will need to manually enter race results.')

        ### Fetch latest race results from Ergast API ###
        race_results = race.fetch_race_results(2024)
        raw_df = pd.DataFrame(race_results)
        
        # remove "Grand Prix" from the raceName
        raw_df['raceName'] = raw_df['raceName'].str.replace(' Grand Prix', '')
        df = raw_df[raw_df["raceName"] == selected_race]
    
        # Join the name and surname
        df['givenName'] = df['givenName'] + ' ' + df['familyName']

        upload_race_results_df = df[['givenName', 'position']].copy()

        # rename 'givenName' to 'driver'
        upload_race_results_df = upload_race_results_df.rename(columns={'givenName': 'driver'})

        st.dataframe(upload_race_results_df, height=738 , hide_index=True)
        submitted = st.form_submit_button("Submit")

        # Process the submitted data
        if submitted:
            circuit_id = fetch_circuit_id(conn, selected_race)
            st.text(selected_race)
            st.text(f'Circuit id: {circuit_id}')
            # Here you can perform any processing or database operations with the submitted data
            for index, row in upload_race_results_df.iterrows():
                driver_name = row['driver']
                position = row['position']
                
            # Database connection
            conn = db.connect_to_postgresql()
            insert_race_results(conn, circuit_id, upload_race_results_df, season)  





    # Display the form with data editor for user input
    with st.form(key='race_results_form'):
        
        st.subheader(":blue[Manual] Entry")
                
        st.caption("Enter '0' if the driver was not part of the race.")
        edited_df = st.data_editor(df_race_results, key='race_results', height=770, hide_index=True)

        submitted = st.form_submit_button("Submit")       
        

    # Process the submitted data
    if submitted:
        circuit_id = fetch_circuit_id(conn, selected_race)
        st.text(selected_race)
        st.text(f'Circuit id: {circuit_id}')
        # Here you can perform any processing or database operations with the submitted data
        for index, row in edited_df.iterrows():
            driver_name = row['driver']
            position = row['position']
            
        # Database connection
        conn = db.connect_to_postgresql()
        insert_race_results(conn, circuit_id, edited_df, season)    
