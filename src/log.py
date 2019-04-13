"""
log

By: Norma Chang
"""
import json
import time


class Log:
    """
    Log class.

    Generates a log file that contains the data from the
    properties of an instance of the leader/follower class.

    Array of dictionaries is generated when the log file is loaded.
    """
    def __init__(self):
        self._start_time = time.strftime('%b %d %Y %H:%M:%S', time.gmtime())

    def log_to_file(self, robot_obj, role):
        """
        Logs data from leader or follower.

        The roles are given in the when the function is called,
        if the roles are given in the proper format the script will
        log the data from the properties of that class instance into
        dictionaries. If the role is not an accepted role or not in
        the correct format, an exception is raised.

        :param robot_obj: Where the instance of the class is passed in.
                          'follower' for the follower class instance
                          and 'leader' for the leader class instance.
        :type robot_obj: object

        :param role: Role of the class instance.
                     'follower' for the follower role
                     and 'leader' for the leader role.
        :type: string
        """
        if role == 'leader':
            leader_dict = {
                'Time': time.time(),
                'Input': robot_obj._distance,
                'Speed': robot_obj._speed,
            }
            self.write_to_file(leader_dict, role)
        elif role == 'follower':
            follower_dict = {
                'Time': time.time(),
                'Distance': robot_obj._distance,
                'Speed': robot_obj._speed,
                'Turn Angle': robot_obj._turn_angle,
                'Yaw': robot_obj._yaw,
            }
            self.write_to_file(follower_dict, role)
        else:
            raise Exception('Role must be leader or follower.'.format(role))


    def write_to_file(self, robot_obj, file_name):
        """
        Write directionary data into text file.

        Opens the file where the name of the file is taken from the role
        and data is appended to the file as the program runs.

        :param robot_obj: Where the instance of the class is passed in.
                          'follower' for the follower class instance
                          and 'leader' for the leader class instance.
        :type robot_obj: object

        :param: file_name: Name of the file which is taken from the role.
        :type: string
        """
        self._start_time = self._start_time.replace(" ", "").replace(":", "")
        with open(file_name + self._start_time + '.log', 'a') as outfile:
            json.dump(robot_obj, outfile)
            outfile.write(',')


    def read_log_file(self, file_name):
        """
        Reads the log file.

        The log file generated from the write_to_file
        function is loaded and parsed. An array of dictionaries
        is returned for interpretational use.

        :param: file_name: Name of the file which is taken from the role.
        :type: string
        """
        try:
            log_file = open(file_name, 'r')
        except:
            print('Error: Check that the log file exists.')

        log = json.loads('['+log_file+']')

        return log
