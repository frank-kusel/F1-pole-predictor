'''
This script contains a list of functions to fetch data
'''

import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

@st.cache_data
def race_schedule(year):
    '''
    Fetch a list of race names and dates using the ergast API
    :param: 
    :return: [ {
                    'raceName': 'Australian Grand Prix',
                    'date': '2023-03-20',
                    'circuitName': 'Albert Park Grand Prix Circuit'
                },
    '''
    
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
                'raceName': race['raceName'].replace( ' Grand Prix', ''),
                'date': race['date'],
                'circuitName': race['Circuit']['circuitName']
            }
            race_schedule.append(race_details)
            
        # print(race_schedule)
        
    else:
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
        print("Error: Unable to retrieve race schedule. Please check your connection or try again later. race_schedule entered manually.")

    return race_schedule

@st.cache_data
def drivers():
    '''
    Fetch list of driver names from ergast API
    :param:
    :return: givenName familyName
    '''
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
        
        # print(driver_names)

    else:
        print("Failed to retrieve driver data from the Ergast API")

    return driver_names


def next_race_name(race_schedule):
    # Get the current date and time
    current_date = datetime.today()

    # Iterate through the race schedule to find the next race
    for race in (race_schedule):
        # Convert the race date string to a datetime object
        race_date = datetime.strptime(race['date'], '%Y-%m-%d')

        # Check if the race date is after the current date
        if race_date.date() >= current_date.date():
            return race['raceName'], race_date.date(), race['circuitName']
        
    # If no future race is found, return None
    return None

