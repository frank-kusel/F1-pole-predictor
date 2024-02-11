'''
This script contains a list of functions to fetch data
'''

import streamlit as st
import requests
import pandas as pd

def race_schedule(year):
    # Define the base URL of the Ergast API
    base_url = "https://ergast.com/api/f1"

    # Endpoint for race schedule for the specified year
    endpoint = f"{base_url}/{year}.json"

    # Make a GET request to the API
    response = requests.get(endpoint)

    # Initialize a list to store race details
    race_schedule = []

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        race_data = response.json()

        # Extract the race schedule from the JSON data
        races = race_data['MRData']['RaceTable']['Races']

        # Populate the race schedule list with race details
        for race in races:
            race_details = {
                'raceName': race['raceName'],
                'date': race['date'],
                'circuitName': race['Circuit']['circuitName']
            }
            race_schedule.append(race_details)
    else:
        print("Error: Unable to retrieve race schedule. Please check your connection or try again later.")



    return race_schedule


def drivers():

    # Define the URL of the Ergast API endpoint for drivers
    url = "http://ergast.com/api/f1/current/drivers.json"

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()

        # Extract the list of driver data from the JSON response
        drivers_data = data["MRData"]["DriverTable"]["Drivers"]

        # Extract the names of the drivers and store them in a list
        driver_names = [driver["givenName"] + " " + driver["familyName"] for driver in drivers_data]
        
        print(driver_names)
        
        # Print the list of driver names

    else:
        print("Failed to retrieve driver data from the Ergast API")

    return driver_names
