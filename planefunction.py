import sys
from geopy.distance import geodesic
from collections import Counter
from pymavlink import mavutil


master = mavutil.mavlink_connection('udpin:localhost:14550')
# Wait a heartbeat before sending commands
master.wait_heartbeat()
print("Mission is initialized")

# OPERATIONAL FUNCTIONS THAT MAKES THE PLANE WORK

# what do you think this does
def changemode(Mode):

    # Check if mode is available
    if Mode not in master.mode_mapping():
        print("test")
        print('Unknown mode : {}'.format(Mode))
        print('Try:', list(master.mode_mapping().keys()))
        sys.exit(1)
    # Get mode ID
    mode_id = master.mode_mapping()[Mode]
    # Set new mode
    # master.mav.command_long_send(
    #    master.target_system, master.target_component,
    #    mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,    
    #    0, mode_id, 0, 0, 0, 0, 0) or:
    # master.set_mode(mode_id) or:
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    print("Mode changed to "+ Mode)

# what do you think this does
def armplane():
    master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    msg = master.recv_match(type="COMMAND_ACK", blocking = True )
    print(msg)

# DIRECTIONAL FUNCTIONS THAT TELL THE PLANE WHERE TO GO

# makes the plane take off you dummy
def takeoffplane():

    master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                                        0, 1, 0, 0, 0, 0, 0, 0)

    msg = master.recv_match(type='COMMAND_ACK', blocking=True)
    print(msg)

    master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                     0, 10, 0, 0, 0, 0, 0, 40)

    msg = master.recv_match(type='COMMAND_ACK', blocking=True)
    print(msg)

# tells the plane to go to coordinates
# go home bruh
def goHome():
      master.mav.command_int_send(master.target_system, master.target_component,
					  mavutil.mavlink.MAV_FRAME_GLOBAL,
                                         mavutil.mavlink.MAV_CMD_DO_REPOSITION, 0, 0, -1, 1, 15, 1, 0, 0, 200)

      print("waypoint set to 0, 0, 200")

# go place bruh (asks for user input for the radius)
def missionStart(latitude: float, longitude: float):
      radius = input("Enter radius: ")
      master.mav.command_int_send(master.target_system, master.target_component,
					  mavutil.mavlink.MAV_FRAME_GLOBAL,
                                         mavutil.mavlink.MAV_CMD_DO_REPOSITION, 0, 0, -1, 1, float(radius), 1, int(latitude * 10**7), int(longitude * 10**7), 200)

      print("waypoint set to " + str(latitude) + ", " + str(longitude) + ", 200")

# go place bruh (preset input for the radius)
def missionStartR(latitude: float, longitude: float, radius: float):
      master.mav.command_int_send(master.target_system, master.target_component,
					  mavutil.mavlink.MAV_FRAME_GLOBAL,
                                         mavutil.mavlink.MAV_CMD_DO_REPOSITION, 0, 0, -1, 1, float(radius), 1, int(latitude * 10**7), int(longitude * 10**7), 200)

      print("waypoint set to " + str(latitude) + ", " + str(longitude) + ", 200")

# basically missionStart, but flies through instead of loitering
def flyThrough(latitude: float, longitude: float,):
     master.mav.command_int_send(master.target_system, master.target_component,
					  mavutil.mavlink.MAV_FRAME_GLOBAL,
                                         mavutil.mavlink.MAV_CMD_DO_REPOSITION, 0, 0, 0, 1, 0, 1, int(latitude * 10**7), int(longitude * 10**7), 200)
     print("waypoint set to " + str(latitude) + ", " + str(longitude) + ", 200")

def geofence(altitude: int, radius: int):
      master.mav.command_int_send(master.target_system, master.target_component,
					  mavutil.mavlink.MAV_FRAME_GLOBAL,
                                         mavutil.mavlink.MAV_CMD_DO_FENCE_ENABLE, 1)

# finds the most common set of coordinates
def most_common_coordinates_separate(latitudes, longitudes, tolerance=1e-6):
    # Round coordinates to a certain tolerance level
    rounded_coords = [(round(lat, 6), round(lon, 6)) for lat, lon in zip(latitudes, longitudes)]

    # Count occurrences of each rounded coordinate
    latitude_counter = Counter(latitudes)
    longitude_counter = Counter(longitudes)

    # Find the most common latitude and longitude
    most_common_latitude, _ = latitude_counter.most_common(1)[0]
    most_common_longitude, _ = longitude_counter.most_common(1)[0]

    return most_common_latitude, most_common_longitude

