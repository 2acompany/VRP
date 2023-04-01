import math

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

# Example locations with latitude and longitude
locations = [
    {'name': 'A', 'lat': 52.3702, 'lon': 4.8952},
    {'name': 'B', 'lat': 51.5074, 'lon': -0.1278},
    {'name': 'C', 'lat': 48.8566, 'lon': 2.3522},
    {'name': 'D', 'lat': 41.9028, 'lon': 12.4964},
    {'name': 'E', 'lat': 40.4168, 'lon': -3.7038},
    {'name': 'F', 'lat': 41.3851, 'lon': 2.1734},
    {'name': 'G', 'lat': 45.4642, 'lon': 9.1900},
    {'name': 'H', 'lat': 52.5200, 'lon': 13.4050},
    {'name': 'I', 'lat': 51.7520, 'lon': -1.2577},
    {'name': 'J', 'lat': 51.5074, 'lon': 0.1278}
]

# Create the time matrix using haversine distance formula
n_nodes = len(locations)
time_matrix = []
for i in range(n_nodes):
    row = []
    for j in range(n_nodes):
        if i == j:
            row.append(0)
        else:
            dist = haversine_distance(locations[i]['lat'], locations[i]['lon'], locations[j]['lat'], locations[j]['lon'])
            dist = int(dist)
            time = dist / 50  # Assuming average speed of 50 km/h
            time=int(time)
            row.append(time)
    time_matrix.append(row)

print(time_matrix)