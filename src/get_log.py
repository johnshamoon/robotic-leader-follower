import json
import time

def follower_log(follower):

    dictionary = {
        'Time' : time.asctime(time.localtime(time.time())), 
        'Distance' : follower._distance,
        'Speed' : follower._speed,
        'Turn Angle' : follower._turn_angle,
        'Yaw' : follower._yaw,
    }
    write_to_file(dictionary)


def write_to_file(data):
    with open('log.txt', 'a') as outfile:
        json.dump(data, outfile, indent=2)
        outfile.write(',\r\n')
 
    
    
