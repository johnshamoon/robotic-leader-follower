"""
log

By: Norma Chang
"""
import json
import time
import os.path


class Log:
    """
    Logging class.

    Logs data from the properties of an instance of an vehicle class for
    testing purposes.
    """
    def __init__(self):

        self.file_name = ""
        self.class_name = ""
        self._start_time = time.strftime('%b %d %Y %H:%M:%S', time.gmtime())
        self._start_time = self._start_time.replace(" ", "").replace(":", "")


    def isFollower(self, vehicle):
        if vehicle.__class__.__name__ == 'Follower':
            return True
        else:
            return False


    def isLeader(self, vehicle):
        if vehicle.__class__.__name__ == 'Leader':
            return True
        else:
            return False


    def log_vehicle_data(self, vehicle):
        """
        Logs vehicle data.

        :param vehicle: The instance of the vehicle class
        :type vehicle: object
        """

        if self.isFollower(vehicle):
            self.class_name = vehicle.__class__.__name__
            self.vehicle_dict = {
                'Time': time.time(),
                'Distance': vehicle._distance,
                'Speed': vehicle._speed,
                'Turn Angle': vehicle._turn_angle,
                'Yaw': vehicle._yaw,
            }
        elif self.isLeader(vehicle):
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
        Reads any log file that conforms to the specified format.

        :param: file_name: File name is generated in log_vehicle_data
                           after verifying the type of vehicle.
        :type: string
        """
        if os.path.isfile(file_name):
            log_file = open(file_name, 'r')
        else:
            raise FileNotFoundError('File does not exist')
        log = json.loads('['+str(log_file)+']')

        return log

def main():
    log = Log()
    lol = log.read_log_file('FollowerApr152019022253.log')
    print(lol)

main()