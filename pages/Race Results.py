'''
This page reveals various race statistics.  
'''

import streamlit as st
import requests
import pandas as pd


# TODO: Add statistics and filter options. 
# TODO: Can pages also have main functions??
# TODO: Filter race by calling a new url, which might be quicker? OR print all previous races to a database


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
        
        # Extract and append race data
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
                    # "speed": result["FastestLap"]["AverageSpeed"]["speed"]
                }
                
                if "speed" in result:
                    race_data["speed"] = result["FastestLap"]["AverageSpeed"]["speed"]
                else:
                    race_data["speed"] = None

                if "Time" in result:
                    race_data["time"] = result["Time"]["time"]
                else:
                    race_data["time"] = None
                
                races.append(race_data)
        
        # Update offset and total_races for pagination
        offset += 100
        total_races = int(data["MRData"]["total"])
        
    return races

def main():
    st.title("Race Results")

    # Divide the app layout into two columns
    col1, col2 = st.columns(2)

    # Select season in the first column
    with col1:
        selected_season = st.selectbox("Select Season", list(range(2024, 1950-1, -1)))

    # Select race in the second column
    with col2:
        # Fetch race results for the selected season
        races = fetch_race_results(selected_season)

        # Create DataFrame
        df = pd.DataFrame(races)

        selected_race = st.selectbox("Select Race", df["raceName"].unique())
 

    # Apply filters
    filtered_df = df[df["raceName"] == selected_race]
    
    
    # Rename columns
    filtered_df = filtered_df.rename(columns={
        "position": "Position",
        "givenName": "Name",
        "familyName": "Surname",
        "time": "Time",
        "grid": "Grid"
    })
    

    # Show filtered DataFrame with specific columns
    if not filtered_df.empty:
        st.dataframe(filtered_df[['Position', 'Grid', 'Name', 'Surname', 'Time']].style.applymap(color_survived, subset=['Position', 'Grid']), use_container_width=True, hide_index=True)
    else:
        st.write("No data available for the selected season and race.")


# Apply custom CSS to highlight cells containing the number 10
def color_survived(val):
    color = 'red' if int(val)==10 else 'black'
    return f'background-color: {color}'

if __name__ == "__main__":
    main()

