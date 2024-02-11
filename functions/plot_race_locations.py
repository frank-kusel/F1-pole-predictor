import folium

# Define the map center
map_center = [20, 0]

# Create a folium map
mymap = folium.Map(location=map_center, zoom_start=2)

# Define the locations
locations = [
    {"lon": 50.512, "lat": 26.031, "location": "Sakhir", "name": "Bahrain International Circuit", "id": "bh-2002"},
    {"lon": 39.104, "lat": 21.632, "location": "Jeddah", "name": "Jeddah Corniche Circuit", "id": "sa-2021"},
    {"lon": 144.970, "lat": -37.846, "location": "Melbourne", "name": "Albert Park Circuit", "id": "au-1953"},
    {"lon": 136.534, "lat": 34.844, "location": "Suzuka", "name": "Suzuka International Racing Course", "id": "jp-1962"},
    {"lon": 121.221, "lat": 31.340, "location": "Shanghai", "name": "Shanghai International Circuit", "id": "cn-2004"},
    {"lon": -80.239, "lat": 25.958, "location": "Miami", "name": "Miami International Autodrome", "id": "us-2022"},
    # Add more locations...
]

# Add markers for each location
for loc in locations:
    folium.Marker([loc['lat'], loc['lon']], popup=loc['name']).add_to(mymap)

# Display the map
mymap
