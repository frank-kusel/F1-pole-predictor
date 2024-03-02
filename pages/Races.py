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
    st.title("Races")

    st.info('View the season :red[**Schedule**] and  :red[**Results**] to compare final race positions vs starting grid positions.')

    st.subheader(':red[Schedule]')
    st.dataframe(race_schedule,
                        column_order=("raceName", "date", "circuitName"), 
                        column_config={
                            "raceName": "Grand Prix",
                            "date": "Date",
                            "circuitName": "Circuit Name"
                        },
                        hide_index=True,
                        height=200, 
                        use_container_width=True)

    st.subheader(":red[Results]")
    st.caption('*(Race results are fetched from somewhere else, and that somewhere else is sometimes not always there. Let the dough rise and come back later.)*')
    try:
        col1, col2 = st.columns(2)

        with col1:
            selected_season = st.selectbox("Select Season", list(range(2024, 2015, -1)))

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
            st.dataframe(filtered_df[['Position', 'Grid', 'Name', 'Surname', 'Time']].style.applymap(color_survived, subset=['Position', 'Grid']), use_container_width=True, hide_index=True, height=738)
        else:
            st.write("No data available for the selected season and race.")
    except:
        st.error("Couldn't find somewhere else. Please try again later :)")



def color_survived(val):
    color = 'red' if int(val) == 10 else 'black'
    return f'background-color: {color}'

race_results()
