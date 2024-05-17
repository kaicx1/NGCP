import time
from planefunction import *
from geopy.distance import geodesic
from read import *

x, y = 1, 1
while True:
    if (getMode() == 11):
        break
missionStartR(x, y, 1984)