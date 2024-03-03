import streamlit as st
import streamlit as st
import psycopg2
import functions.database as db
import functions.ergast as erg
import pandas as pd

st.title("Features")

st.markdown('Keep an eye on this space for new features and updates...')


st.markdown('#### :green[Updates]')
st.text('2024-03-03 : Points column added to view how many points your previous picks scored.')   
st.text('2024-03-02 : Races Page added.')



# Sample list of driver names
driver_names = erg.drivers()
if driver_names is None:
    driver_names = ("Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Zhou Guanyu", "Oscar Piastri", "Sergio Perez", "Charles Leclerc", "Daniel Ricciardo", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso", "Esteban Ocon", "Lance Stroll", "Yuki Tsunoda", "George Russell", "Alex Albon", "Logan Sargeant", "Kevin Magnussen", "Nico Hulkenberg")
    

# Create a DataFrame to hold the data
df_race_results = pd.DataFrame({
    'Driver': driver_names,
    'Position': [None] * len(driver_names)
})


# Create admin section
password = 'cakecakecake'

key = st.text_input('Admin:')

if key == password:

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
    with st.form(key='race_results_form'):
        
        st.error('*:red[This form uploads and overwrites race results for the selected race and season. Use with caution!]*')
        
        # Display the data editor for user input
        season = st.text_input('Season (year)')
        circuit_id = st.selectbox('Circuit Name:', race_names)
        
        edited_df = st.data_editor(df_race_results, key='race_results', height=770)

        # Add a submit button
        submitted = st.form_submit_button("Submit")

    # Process the submitted data
    if submitted:
        # Here you can perform any processing or database operations with the submitted data
        for index, row in edited_df.iterrows():
            driver_name = row['Driver']
            position = row['Position']
            # Perform your operations here, like inserting into a database, etc.
            st.write(f"Driver: {driver_name}, Position: {position}")


    # # Function to insert race results into the database
    # def insert_race_results(conn, df_race_results):
    #     try:
    #         with conn.cursor() as cursor:
    #             # Delete existing race results for the given season
    #             cursor.execute("DELETE FROM race_results WHERE season = %s", (df_race_results.loc[0, 'Season'],))

    #             # Insert new race results into the database
    #             for index, row in df_race_results.iterrows():
    #                 cursor.execute(
    #                     "INSERT INTO race_results (position, driver, season) VALUES (%s, %s, %s)",
    #                     (row['Position'], row['Driver'], df_race_results.loc[0, 'Season'])
    #                 )

    #         # Commit the transaction
    #         conn.commit()
    #         st.success("Race results submitted successfully!")
    #     except Exception as e:
    #         st.error(f"Error: {e}")

