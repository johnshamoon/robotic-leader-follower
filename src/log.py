"""
log

Author: Norma Chang
"""
import json
import os.path
import time


class Log:
    """
    Logging class.

    Logs data from vehicle.
    """
    def __init__(self, name):
        self.file_name = ""
        self._start_time = time.strftime('%b %d %Y %H:%M:%S', time.gmtime())
        self._start_time = self._start_time.replace(" ", "").replace(":", "")

        self.file_name = name + self._start_time + '.log'


    def write_to_file(self, dictionary):
        """
        Write dictionary into text file.

        :param: dictionary: The dictionary passed in from a class. 
        :type: dict
        """
        dictionary['time'] = time.time()
        with open(self.file_name, 'a') as outfile:
            json.dump(dictionary, outfile)
            outfile.write(',')


    def read_log_file(self, file_name):
        """
        Reads any log file that conforms to the specified format.

        :param: file_name: The given file name in a valid format.
        :type: string

        :return: An array of dictionaries
        """
        if os.path.isfile(file_name):
            log_file = open(file_name, 'r').read()
        else:
            # Raise error if file fails to open.
            raise IOError("File does not exist")
        # Loads the log file as JSON.
        log = json.loads('['+log_file+']')

        return log
