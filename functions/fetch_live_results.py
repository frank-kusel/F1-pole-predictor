'''
Fetch live results to be used for points calculations
'''

import requests

def calculate_points(driver1_guess, driver2_guess, position_guess, points_system_url):
    # Fetch the latest race results from the ERGAST API
    response = requests.get(points_system_url)
    if response.status_code != 200:
        print("Failed to fetch race results from ERGAST API")
        return None
    
    race_results = response.json()  # Assuming the response is in JSON format
    
    # Extract the position and points data from the race results
    position_data = race_results.get("Position")
    points_data = race_results.get("Points")
    
    if not position_data or not points_data:
        print("No race results data found")
        return None
    
    # Create a dictionary to map positions to points
    position_points_map = {position: points for position, points in zip(position_data, points_data)}
    
    # Calculate points for driver 1 guess
    driver1_points = position_points_map.get(driver1_guess, 0)
    
    # Calculate points for driver 2 guess (points halved)
    driver2_points = position_points_map.get(driver2_guess, 0) / 2
    
    # Calculate points for position guess
    position_points = position_points_map.get(position_guess, 0)
    
    # Calculate the maximum points for each driver guess
    max_driver1_points = max(driver1_points, position_points)
    max_driver2_points = max(driver2_points, position_points)
    
    return max_driver1_points, max_driver2_points
