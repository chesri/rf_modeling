import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # radius of the Earth in kilometers

    # convert latitudes and longitudes to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # calculate the differences between latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # calculate the haversine of the differences
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2

    # calculate the great circle distance in kilometers
    distance = 2 * R * math.asin(math.sqrt(a))

    # convert kilometers to meters
    distance *= 1000

    return distance

lat1 = 35.1173620            #  79.1306856°W 35.1173620°N
lon1 = -79.1306856
lat2 = 35.1505534               # 79.0876685°W 35.1505534°N
lon2 = -79.0876685
distance = haversine_distance(lat1, lon1, lat2, lon2)
print(distance)