import time
from planefunction import *

armplane()
mode = "TAKEOFF"
changemode(mode)

takeoffplane()
time.sleep(10)

mode = "AUTO"
changemode(mode)

missionStart()