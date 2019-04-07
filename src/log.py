"""
Data Log

By: Norma Chang
"""
import json
import time

def log(data, data_type):
    """
    Logs dictionary data from leader
    """
    if data_type == 'leader':
        leader_dict = {
            'Time' : time.time(), 
            'Input' : data._distance,
            'Speed' : data._speed,
        }
        write_to_file(leader_dict, data_type)
    elif data_type == 'follower':
        follower_dict = {
            'Time' : time.time(), 
            'Distance' : data._distance,
            'Speed' : data._speed,
            'Turn Angle' : data._turn_angle,
            'Yaw' : data._yaw,
        }
        write_to_file(follower_dict, data_type)
    else:
        pass

def write_to_file(data, file_name):
    """
    Write directionary data to text file.
    """
    with open(file_name + '.log', 'a') as outfile:
        json.dump(data, outfile)
        outfile.write('\n')

def array_dict(file_name):
  """
  Returns the log file containing the cycle data.
  """
  string_arr = []
  array_dict = []

  log_file = open(file_name, 'r')
  log = log_file.read().strip().split('\n')

  for line in log:
    string_arr.append(line)

  for string in string_arr:
    dictionary = json.loads(string)
    array_dict.append(dictionary)