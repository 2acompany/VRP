import math

def get_time_matrix(locations):
    def haversine_distance(loc1, loc2):
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        # Convert latitude and longitude to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r

    # Create the time matrix using haversine distance formula
    n_nodes = len(locations)
    time_matrix = []
    for i in range(n_nodes):
        row = []
        for j in range(n_nodes):
            if i == j:
                row.append(0)
            else:
                dist = haversine_distance(locations[i], locations[j])
                time = dist / 50  # Assuming average speed of 50 km/h
                time = int(time * 60) # Convert time to minutes
                row.append(time)
        time_matrix.append(row)

    return time_matrix


locations = [
    (35.7262191, 61.5617297), # Tehran 01
    (35.738501, 61.479981), # Tehran 02
    (35.733694, 61.536736), # Tehran 03
    (35.748602, 61.553323),  # Tehran 04
    (35.724165, 61.524634) # Tehran 05
]

time_matrix = get_time_matrix(locations)

print(time_matrix)
