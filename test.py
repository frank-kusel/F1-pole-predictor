import streamlit as st
import pandas as pd
import psycopg2
from datetime import date
from datetime import datetime

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

