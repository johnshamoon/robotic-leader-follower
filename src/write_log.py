"""
Write Log File

By: Norma Chang
"""
import json
import time
import read_log as read

def follower_log(follower):
    """
    Logs dictionary data from follower
    """
    follower_dict = {
        'Time' : time.asctime(time.localtime(time.time())), 
        'Distance' : follower._distance,
        'Speed' : follower._speed,
        'Turn Angle' : follower._turn_angle,
        'Yaw' : follower._yaw,
    }
    write_to_file(follower_dict)

def leader_log(leader):
    """
    Logs dictionary data from leader
    """
    leader_dict = {
        'Time' : time.asctime(time.localtime(time.time())), 
        'Input' : leader._distance,
        'Speed' : leader._speed,
    }
    write_to_file(leader_dict)

def write_to_file(data):
    """
    Write directionary data to text file.
    """
    with open('log.txt', 'a') as outfile:
        json.dump(data, outfile)
        outfile.write('\n')

def start_log(follower):
    follower_log(follower)
    read.read_file()