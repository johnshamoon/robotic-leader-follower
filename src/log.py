"""
log

By: Norma Chang
"""
import json
import os.path
import time


class Log:
    """
    Logging class.

    Logs data from vehicle.
    """
    def __init__(self):

        self.file_name = ""
        self.class_name = ""
        self._start_time = time.strftime('%b %d %Y %H:%M:%S', time.gmtime())
        self._start_time = self._start_time.replace(" ", "").replace(":", "")


    def is_follower(self, vehicle):
        if vehicle.__class__.__name__ == 'Follower':
            return True
        else:
            return False


    def is_leader(self, vehicle):
        if vehicle.__class__.__name__ == 'Leader':
            return True
        else:
            return False


    def log_vehicle_data(self, vehicle):
        """
        Logs vehicle data.

        :param vehicle: Instance of a vehicle class.
        :type vehicle: Dictionary
        """
        if self.is_follower(vehicle):
            self.class_name = vehicle.__class__.__name__
            self.vehicle_dict = {
                'Time': time.time(),
                'Distance': vehicle._distance,
                'Speed': vehicle._speed,
                'Turn Angle': vehicle._turn_angle,
                'Yaw': vehicle._yaw,
            }
        elif self.is_leader(vehicle):
            self.class_name = vehicle.__class__.__name__
            self.vehicle_dict = {
                'Time': time.time(),
                'Input': vehicle.turn(position),
                'Speed': vehicle.set_speed(position),
            }
        else:
            raise ValueError('Unexpected class type')

        self.file_name = self.class_name + self._start_time + '.log'
        self.write_to_file()


    def write_to_file(self):
        """
        Write vehicle data into text file.
        """
        with open(self.file_name, 'a') as outfile:
            json.dump(self.vehicle_dict, outfile)
            outfile.write(',')


    def read_log_file(self, file_name):
        """
        Reads the log file.

        :param: file_name: Unique, auto-generated file name.
        :type: string
        """
        if os.path.isfile(file_name):
            log_file = open(file_name, 'r')
        else:
            raise IOError("File does not exist")
        # Loads the log file and converts strings to
        # valid JSON format.
        log = json.loads('['+log_file+']')

        return log
