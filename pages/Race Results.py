'''
This page reveals the race results. 
# TODO: Figure out how to use ErgastAPI for past race results. 
# TODO: Figure out how to update live race stats. 

For now this page is on its own to figure out how the Ergast API works. 
'''

import streamlit as st
import requests
import pandas as pd

# # --- Sidebar ---
# st.sidebar.markdown("## Last Race Results 🏁")

# # --- Tabs ---
# tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
# tab1.write("This is a tab")
# tab2.write("And another onw!")

# # --- Container ---
# c = st.container(border=True)
# c.markdown("Race Results 🏁")
# c.markdown("Show results")
# st.markdown("# Race Results 🏁")



# # --- Get list of drivers and their stats from the F1 data API
# url = "http://ergast.com/api/f1/2023/last/drivers.json" # this API will be shut down end of 2024 :(
# response = requests.get(url)
# data = response.json()

# # Convert the data to a pandas DataFrame
# drivers = pd.DataFrame(data["MRData"]["DriverTable"]["Drivers"])
# drivers["Name"] = drivers["givenName"] + " " + drivers["familyName"]
# st.dataframe(drivers)






# # Function to fetch race results with pagination and filter by circuit name
# def fetch_race_results():
#     url = "http://ergast.com/api/f1/2023/results.json"
#     all_results = []

#     page = 1
#     while True:
#         params = {"page": page}
#         response = requests.get(url, params=params)
#         data = response.json()

#         # Check if there are results on this page
#         if "MRData" in data and "RaceTable" in data["MRData"] and "Races" in data["MRData"]["RaceTable"]:
#             all_results.extend(data["MRData"]["RaceTable"]["Races"])

#         # Check if there are more pages to retrieve
#         if "MRData" in data and "RaceTable" in data["MRData"] and "total" in data["MRData"]["RaceTable"]:
#             total_races = int(data["MRData"]["RaceTable"]["total"])
#             per_page = int(data["MRData"]["RaceTable"]["limit"])
#             if (page * per_page) < total_races:
#                 page += 1
#             else:
#                 break
#         else:
#             break

#     # Process all_results and create DataFrame
#     df = pd.DataFrame(all_results)
#     return df


# # Fetch race results and filter by circuit name
# def load_data():
#     df = fetch_race_results()
#     return df


# def main():
#     st.title("F1 Race Results")
#     st.markdown("Explore race results from the Formula 1 season.")

#     # Load race results data
#     df = load_data()

#     # Filter by circuit name
#     circuit_names = df["Circuit"].unique()
#     selected_circuit = st.selectbox("Select Circuit", circuit_names)

#     filtered_df = df[df["Circuit"] == selected_circuit]

#     # Display filtered results
#     st.dataframe(filtered_df)

# if __name__ == "__main__":
#     main()











# import requests
# import pandas as pd

# def fetch_race_results():
#     base_url = "http://ergast.com/api/f1/"
#     season = "2023"  # Change to the desired season
#     races = []
    
#     # Fetch race results using pagination
#     offset = 0
#     limit = 30  # Number of results per page
#     total_races = float('inf')  # Initially set to infinity to start the loop
    
#     while offset < total_races:
#         url = f"{base_url}{season}/results.json?limit={limit}&offset={offset}"
#         response = requests.get(url)
#         data = response.json()
        
#         total_races = int(data["MRData"]["total"])
#         offset += limit
        
#         for race in data["MRData"]["RaceTable"]["Races"]:
#             for result in race["Results"]:
#                 races.append({
#                     "season": race["season"],
#                     "round": race["round"],
#                     "raceName": race["raceName"],
#                     "circuitID": race["Circuit"]["circuitId"],
#                     "country": race["Circuit"]["Location"]["country"],
#                     "date": race["date"],
#                     "driverID": result["Driver"]["driverId"],
#                     "position": result["position"],
#                     "constructorID": result["Constructor"]["constructorId"],
#                     # "time": result["Time"]["time"]
#                 })

#     return pd.DataFrame(races)

# def main():
#     race_results = fetch_race_results()
#     st.dataframe(race_results)
#     print(race_results)

# if __name__ == "__main__":
#     main()
















# import streamlit as st
# import requests
# import pandas as pd

# def fetch_race_results():
#     base_url = "http://ergast.com/api/f1/"
#     season = "2008"  # Change to the desired season
#     races = []
    
#     # Fetch race results using pagination
#     offset = 0
#     limit = 30  # Number of results per page
#     total_races = float('inf')  # Initially set to infinity to start the loop
    
#     while offset < total_races:
#         url = f"{base_url}{season}/results.json?limit={limit}&offset={offset}"
#         response = requests.get(url)
#         data = response.json()
        
#         race_table = data.get("MRData", {}).get("RaceTable", {})
#         if not race_table:
#             break  # Exit the loop if no race table is found
        
#         total_races = int(race_table.get("total", 0))
#         offset += limit
        
#         races.extend(extract_race_data(race_table))

#     return pd.DataFrame(races)

# def extract_race_data(race_table):
#     races = []
#     for race in race_table.get("Races", []):
#         for result in race.get("Results", []):
#             race_data = {
#                 "season": race["season"],
#                 "round": race["round"],
#                 "raceName": race["raceName"],
#                 "circuitID": race["Circuit"]["circuitId"],
#                 "country": race["Circuit"]["Location"]["country"],
#                 "date": race["date"],
#                 "driverID": result["Driver"]["driverId"],
#                 "position": result["position"],
#                 "constructorID": result["Constructor"]["constructorId"],   
#                 "status": result["status"]
#             }
#             # Check if the 'Time' key exists
#             if "Time" in result:
#                 race_data["time"] = result["Time"]["time"]
#             else:
#                 race_data["time"] = None  # Set to None if the key is missing
#             races.append(race_data)
#     return races


# def main():
#     st.title("F1 Race Results")
#     race_results = fetch_race_results()
#     st.dataframe(race_results)

# if __name__ == "__main__":
#     main()



import streamlit as st
import pandas as pd
import requests

@st.cache
def fetch_race_results():
    # Define the API URL
    url = "http://ergast.com/api/f1/2023/results.json"
    response = requests.get(url)
    data = response.json()
    race_table = data["MRData"]["RaceTable"]
    return race_table

def extract_race_data(race_table):
    races = []
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
                "position": result["position"],
                "constructorID": result["Constructor"]["constructorId"]
            }
            if "Time" in result:
                race_data["time"] = result["Time"]["time"]
            else:
                race_data["time"] = None
            races.append(race_data)
    return races

def main():
    st.title("Formula 1 Race Results")

    # Fetch race results
    race_table = fetch_race_results()
    races = extract_race_data(race_table)

    # Create DataFrame
    df = pd.DataFrame(races)

    # Filter by season
    selected_season = st.selectbox("Select Season", df["season"].unique())

    # Filter by raceName
    selected_race = st.selectbox("Select Race", df["raceName"].unique())

    # Apply filters
    filtered_df = df[(df["season"] == selected_season) & (df["raceName"] == selected_race)]

    # Display filtered DataFrame
    st.write(filtered_df)

if __name__ == "__main__":
    main()
