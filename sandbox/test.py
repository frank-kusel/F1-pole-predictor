
import requests

import requests

def fetch_latest_race_results():
    # API endpoint for the latest race results
    url = "https://ergast.com/api/f1/current/last/results.json"

    # Make the API call
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract race results from the response JSON
        race_results = response.json()["MRData"]["RaceTable"]["Races"][0]["Results"]
        
        # Create a list to store driver names and positions
        driver_positions = []
        
        # Iterate over each result to extract driver name and position
        for result in race_results:
            driver_name = result["Driver"]["givenName"] + " " + result["Driver"]["familyName"]
            position = result["position"]
            
            # Append driver name and position to the list
            driver_positions.append({"Driver": driver_name, "Position": position})
        
        return driver_positions
    else:
        print("Failed to fetch race results")
        return None

# Test the function
latest_race_results = fetch_latest_race_results()
print(latest_race_results)



def get_driver_position(driver, race_results):
    # Iterate over each race result
    for result in race_results:
        # Check if the driver name matches
        if result["Driver"] == driver:
            # Return the driver's finishing position
            return result["Position"]
    
    # If the driver is not found, return None
    return None

# Test the function
driver = "Lewis Hamilton"
position = get_driver_position(driver, latest_race_results)
print(f"{driver} finished in position {position} in the latest race.")

