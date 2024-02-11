'''
Fetch live results to be used for points calculations
'''

import requests

import requests

def get_driver_position(driver, race_results):
    # Implement function to retrieve driver's position from race results
    # Search race results for driver and return their finishing position
    # Iterate over each race result
    for result in race_results:
        # Check if the driver name matches
        driver_name = result["Driver"]["givenName"] + " " + result["Driver"]["familyName"]
        if driver_name == driver:
            # Return the driver's finishing position
            return result["position"]
    
    # If the driver is not found, return None
    return None

def main(user_id, driver1, driver2):
    '''
    calculate points based on guess
    :param user_id:
    :param driver1:
    :param driver2:
    '''
    # Step 1: Retrieve latest race results from Ergast API
    url = "https://ergast.com/api/f1/current/last/results.json"
    response = requests.get(url)

    if response.status_code == 200:
        race_results = response.json()["MRData"]["RaceTable"]["Races"][0]["Results"]
    else:
        print("Failed to fetch race results")
        return 0

    # Step 2: Compare user's guesses with actual race results
    driver1_position = get_driver_position(driver1, race_results)
    driver2_position = get_driver_position(driver2, race_results)

    # Step 3: Calculate points based on the provided scoring system
    points_system = {
        "10": 25,
        "11": 18,
        "9": 15,
        "12": 12,
        "8": 10,
        "13": 8,
        "7": 6,
        "14": 4,
        "6": 2,
        "15": 1,
        "5": 0.5
    }
    
    # Calculate points for each driver's guess
    driver1_points = points_system.get(driver1_position, 0)
    driver2_points = points_system.get(driver2_position, 0) / 2

    # Return the maximum points between driver1_points and driver2_points
    return max(driver1_points, driver2_points)

# Test the function
# user_id = 1
# driver1 = "Esteban Ocon"
# driver2 = "Lance Stroll"
# print("Maximum Points:", main(user_id, driver1, driver2))


