import streamlit as st
import pandas as pd
import psycopg2
from datetime import date
from datetime import datetime
import functions.database as db


st.markdown('Keep an eye on this space for new features and updates...')

st.markdown('#### :green[Updates]')
st.text('2024-03-03 : Points column added to view how many points your previous picks scored.')   
st.text('2024-03-02 : Races Page added.')

# conn = db.connect_to_postgresql()
# db.update_points_in_user_guesses(conn)


# def connect_to_postgresql():
#     conn = psycopg2.connect(
#         dbname=st.secrets.postgresql.database,
#         user=st.secrets.postgresql.username,
#         password=st.secrets.postgresql.password,
#         host=st.secrets.postgresql.host,
#         port=st.secrets.postgresql.port
#     )
#     return conn

# conn = connect_to_postgresql()



# def generate_leaderboard(conn, year):
#     # Query the database to get the total points for each user_id and their username
#     query = """
#         SELECT u.username, SUM(ug.points) AS total_points
#         FROM user_guesses AS ug
#         INNER JOIN users AS u ON ug.user_id = u.user_id
#         WHERE EXTRACT(YEAR FROM ug.submission_time) = %s
#         GROUP BY ug.user_id, u.username
#     """
    
#     # Execute the query with the year parameter and fetch the results into a DataFrame
#     user_points_df = pd.read_sql_query(query, conn, params=(year,))
    
#     # Add a 'Position' column based on the points
#     user_points_df['Position'] = user_points_df['total_points'].rank(ascending=False, method='dense').astype(int)
    
#     # Select only the required columns 'Name' and 'Points', and order by 'Points' descending
#     leaderboard_df = user_points_df[['Position', 'username', 'total_points']].sort_values(by='total_points', ascending=False)
    
#     # Rename the columns for clarity
#     leaderboard_df.rename(columns={'username': 'Name', 'total_points': 'Points'}, inplace=True)
    
#     return leaderboard_df

# # Example usage:
# # Assuming you have a database connection named 'conn' and 'st' for displaying the DataFrame

# year = 2024  # Example year, change it accordingly
# leaderboard_df = generate_leaderboard(conn, year)
# st.dataframe(leaderboard_df)










# # Connect to PostgreSQL
# def connect_to_postgresql():
#     conn = psycopg2.connect(
#         dbname=st.secrets.postgresql.database,
#         user=st.secrets.postgresql.username,
#         password=st.secrets.postgresql.password,
#         host=st.secrets.postgresql.host,
#         port=st.secrets.postgresql.port
#     )
#     return conn

# def add_points_column(_conn):
#     # Define the SQL query to add the points column to the user_guesses table
#     query = """
#     ALTER TABLE user_guesses
#     ADD COLUMN IF NOT EXISTS points FLOAT;
#     """

#     # Execute the ALTER TABLE query
#     with _conn.cursor() as cursor:
#         cursor.execute(query)
#         _conn.commit()

# conn = connect_to_postgresql()
# add_points_column(conn)

'''
Fetch race results from 2023
'''
# import requests

# def fetch_race_results(season):
#     races = []
#     offset = 0
#     total_races = 30 
    
#     while len(races) < total_races:
#         url = f"http://ergast.com/api/f1/{season}/results.json?limit=100&offset={offset}"
#         response = requests.get(url)
#         data = response.json()
#         race_table = data["MRData"]["RaceTable"]
        
#         for race in race_table.get("Races", []):
#             for result in race.get("Results", []):
#                 race_data = {
#                     "season": race["season"],
#                     "round": race["round"],
#                     "raceName": race["raceName"],
#                     "circuitID": race["Circuit"]["circuitId"],
#                     "country": race["Circuit"]["Location"]["country"],
#                     "date": race["date"],
#                     "driverID": result["Driver"]["driverId"],
#                     "givenName": result["Driver"]["givenName"],
#                     "familyName": result["Driver"]["familyName"],
#                     "position": result["position"],
#                     "constructorID": result["Constructor"]["constructorId"],
#                     "grid": result["grid"]
#                 }
                
#                 race_data["speed"] = result["FastestLap"]["AverageSpeed"]["speed"] if "speed" in result else None
#                 race_data["time"] = result["Time"]["time"] if "Time" in result else None
                
#                 races.append(race_data)
        
#         offset += 100
#         total_races = int(data["MRData"]["total"])
        
#     return races

# fetch_race_results(2023)


# import pandas as pd
# import requests

# def fetch_race_results(season):
#     races = []
#     offset = 0
#     total_races = 30 
    
#     while len(races) < total_races:
#         url = f"http://ergast.com/api/f1/{season}/results.json?limit=100&offset={offset}"
#         response = requests.get(url)
#         data = response.json()
#         race_table = data["MRData"]["RaceTable"]
        
#         for race in race_table.get("Races", []):
#             for result in race.get("Results", []):
#                 race_data = {
#                     "season": race["season"],
#                     "raceName": race["raceName"],
#                     "driver": f"{result['Driver']['givenName']} {result['Driver']['familyName']}",
#                     "position": result["positionText"],
#                     "time": result["Time"]["time"] if "Time" in result else None,
#                     "fastest lap": result.get("FastestLap", {}).get("Time", {}).get("time", None),
#                     "average speed": result.get("FastestLap", {}).get("AverageSpeed", {}).get("speed", None)
#                 }
                
#                 races.append(race_data)
        
#         offset += 100
#         total_races = int(data["MRData"]["total"])
        
#     return races

# # Convert the data into a DataFrame
# race_results = fetch_race_results(2023)
# df = pd.DataFrame(race_results)
# print(df)

# # Export DataFrame to Excel file
# excel_file = 'race_results_2023.xlsx'
# df.to_excel(excel_file, index=False)

# print(f"Race results for 2023 have been exported to {excel_file}.")

