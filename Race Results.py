'''
This page reveals various race statistics.  
'''

import streamlit as st
import requests
import pandas as pd


# TODO: Add statistics and filter options. 
# TODO: Can pages also have main functions??
# TODO: Filter race by calling a new url, which might be quicker? OR print all previous races to a database
# TODO: Show a table showing all past race results and driver positions in order of driver points

@st.cache_data
def fetch_race_results(season):
    races = []
    offset = 0
    total_races = 30 
    
    while len(races) < total_races:
        url = f"http://ergast.com/api/f1/{season}/results.json?limit=100&offset={offset}"
        response = requests.get(url)
        data = response.json()
        race_table = data["MRData"]["RaceTable"]
        
        for race in race_table.get("Races", []):
            for result in race.get("Results", []):
                race_data = {
                    "season": race["season"],
                    "round": race["round"],
                    "raceName": race["raceName"],
                    "circuitID": race["Circuit"]["circuitId"],
                    "country": race["Circuit"]["Location"]["country"],
                    "date": race["date"],
                    "driverID": result["Driver"]["driverId"],
                    "givenName": result["Driver"]["givenName"],
                    "familyName": result["Driver"]["familyName"],
                    "position": result["position"],
                    "constructorID": result["Constructor"]["constructorId"],
                    "grid": result["grid"]
                }
                
                race_data["speed"] = result["FastestLap"]["AverageSpeed"]["speed"] if "speed" in result else None
                race_data["time"] = result["Time"]["time"] if "Time" in result else None
                
                races.append(race_data)
        
        offset += 100
        total_races = int(data["MRData"]["total"])
        
    return races

def race_results():
    if st.button("Home"):
        st.switch_page("F1.py")
    st.title("Race Results")

    st.info('View the results of past races, and compare final race final positions with the starting grid position ')

    col1, col2 = st.columns(2)

    with col1:
        selected_season = st.selectbox("Select Season", list(range(2023, 1950-1, -1)))

    with col2:
        races = fetch_race_results(selected_season)
        df = pd.DataFrame(races)
        selected_race = st.selectbox("Select Race", df["raceName"].unique())

    filtered_df = df[df["raceName"] == selected_race]
    
    filtered_df = filtered_df.rename(columns={
        "position": "Position",
        "givenName": "Name",
        "familyName": "Surname",
        "time": "Time",
        "grid": "Grid"
    })

    if not filtered_df.empty:
        st.dataframe(filtered_df[['Position', 'Grid', 'Name', 'Surname', 'Time']].style.applymap(color_survived, subset=['Position', 'Grid']), use_container_width=True, hide_index=True, height=737)
    else:
        st.write("No data available for the selected season and race.")

def color_survived(val):
    color = 'red' if int(val) == 10 else 'black'
    return f'background-color: {color}'

race_results()
