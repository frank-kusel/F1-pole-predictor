import sandbox.streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime
import numpy as np
import requests
import openpyxl as xl

# # --- Get list of drivers and their stats from the F1 data API
# url = "http://ergast.com/api/f1/2023/last/drivers.json" # this API will be shut down end of 2024 :(
# response = requests.get(url)
# data = response.json()

# # Convert the data to a pandas DataFrame
# drivers = pd.DataFrame(data["MRData"]["DriverTable"]["Drivers"])
# drivers["name"] = drivers["givenName"] + " " + drivers["familyName"] #concatenate the driver name
# print(drivers)

# drivers.to_excel("driver_data.xlsx", index=False)


### --------------------------------- ###

# Define the URL for the Ergast API endpoint


# # Define the season and round of the race you're interested in
# url = "http://ergast.com/api/f1/2023/results.json"

# # Make the HTTP request to the API
# response = requests.get(url)
# data = response.json()
# data_df = pd.DataFrame(data["MRData"]["RaceTable"]["Races"])
# # Further processing or display of race times
# print(data_df)

# data_df.to_excel("race_results.xlsx", index=False)

import requests
import pandas as pd

# Define the URL for the Ergast API endpoint for 2023 race results
url = "http://ergast.com/api/f1/2023/results.json"

# Make the HTTP request to the API
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract race information if available
    if "MRData" in data and "RaceTable" in data["MRData"] and "Races" in data["MRData"]["RaceTable"]:
        races = data["MRData"]["RaceTable"]["Races"]

        # Initialize lists to store race results
        race_results = []

        # Extract race results for each race
        for race in races:
            race_name = race["raceName"]
            race_date = race["date"]

            # Extract driver positions for the race
            results = race["Results"]
            driver_positions = [{"driver": result["Driver"]["givenName"] + " " + result["Driver"]["familyName"],
                                 "position": result["position"]} for result in results]

            # Append race results to the list
            race_results.append({"Race": race_name, "Date": race_date, "Results": driver_positions})

        # Create a DataFrame from the race results
        race_results_df = pd.DataFrame(race_results)
        print(race_results_df.head())
    else:
        print("Race data not found in the response.")

else:
    print("Error: Unable to retrieve race data. Status code:", response.status_code)

race_results_df.to_excel("race_results.xlsx", index=False)