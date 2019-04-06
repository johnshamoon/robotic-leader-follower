"""
Read Log File

By: Norma Chang
"""
import json
import time

def read_file():
  """
  Read the log file containing the cycle data.
  """
  string_arr = []
  array_dict = []

  log_file = open('log.txt', 'r')
  log = log_file.read().strip().split('\n')

  for line in log:
    string_arr.append(line)

  for string in string_arr:
    dictionary = json.loads(string)
    array_dict.append(dictionary)