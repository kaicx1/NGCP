import time
from planefunction import *
from geopy.distance import geodesic
from read import *

filename = "kraken_3.csv"

armplane()
mode = "TAKEOFF"
changemode(mode)

takeoffplane()
time.sleep(3)

mode = "AUTO"
changemode(mode)

missionStartR(34.04328, -117.812824, 30)
print("loitering.......")
time.sleep(20)

lat, long, bearing, accur = read_csv_live("kraken_2.csv")

finallat = []
finallong = []
for i in range(len(lat) - 1):
    point1 = (lat[i], long[i])
    point2 = (lat[i + 1], long[i + 1])
    distance = geodesic(point1, point2).meters  # Calculate distance between points in meters
    bearing1_2 = bearing[i]
    bearing2_1 = (bearing[i] + 180) % 360  # Reverse bearing for the opposite direction
    
    # Calculate the destination point based on the distance and initial bearing
    dest_point = geodesic(kilometers=distance/1000).destination(point1, bearing1_2)
    
    finallat.append(dest_point.latitude)
    finallong.append(dest_point.longitude)


realat, realot = most_common_coordinates_separate(finallat, finallong, tolerance=1e-6)

flyThrough(realat,realot)
