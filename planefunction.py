import sys
from pymavlink import mavutil


master = mavutil.mavlink_connection('udpin:localhost:14550')
# Wait a heartbeat before sending commands
master.wait_heartbeat()
print("Mission is initialized")

# OPERATIONAL FUNCTIONS THAT MAKES THE PLANE WORK

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

def armplane():
    master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    msg = master.recv_match(type="COMMAND_ACK", blocking = True )
    print(msg)


def disarmplane():
    # Disarm
    # master.arducopter_disarm() or:
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        0, 0, 0, 0, 0, 0, 0)

    # wait until disarming confirmed
    master.motors_disarmed_wait()

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
def missionStart():
      master.mav.command_int_send(master.target_system, master.target_component,
					  mavutil.mavlink.MAV_FRAME_GLOBAL,
                                         mavutil.mavlink.MAV_CMD_DO_REPOSITION, 0, 0, -1, 1, 15, 1, 0, 0, 200)

      print("waypoint set")

def mission(latitude, longitude):
      master.mav.command_int_send(master.target_system, master.target_component,
					  mavutil.mavlink.MAV_FRAME_GLOBAL,
                                         mavutil.mavlink.MAV_CMD_DO_REPOSITION, 0, 0, -1, 1, 15, 1, latitude, longitude, 200)

      print("waypoint set")