from numpy import pi
from controller import Keyboard
from vehicle import Driver

ego_vehicle = Driver()
keyboard = Keyboard()
keyboard.enable(int(ego_vehicle.getBasicTimeStep()))

SPEED = 25
FORWARD_RIGHT = pi / 8
FORWARD_LEFT = -FORWARD_RIGHT
BACKWARD_RIGHT = -FORWARD_RIGHT
BACKWARD_LEFT = -FORWARD_LEFT
RIGHT = pi / 4
LEFT = -RIGHT
FORWARD = 0
BACKWARD = -FORWARD
NEUTRAL = 0
SIGNALS = {
    (-1, -1): (NEUTRAL, NEUTRAL),

    (keyboard.LEFT, -1): (NEUTRAL, LEFT),
    (-1, keyboard.LEFT): (NEUTRAL, LEFT),

    (keyboard.RIGHT, -1): (NEUTRAL, RIGHT),
    (-1, keyboard.RIGHT): (NEUTRAL, RIGHT),

    (keyboard.UP, -1): (SPEED, FORWARD),
    (-1, keyboard.UP): (SPEED, FORWARD),

    (keyboard.DOWN, -1): (-SPEED, BACKWARD),
    (-1, keyboard.DOWN): (-SPEED, BACKWARD),

    (keyboard.UP, keyboard.RIGHT): (SPEED, FORWARD_RIGHT),
    (keyboard.RIGHT, keyboard.UP): (SPEED, FORWARD_RIGHT),
    (keyboard.DOWN, keyboard.RIGHT): (-SPEED, BACKWARD_RIGHT),
    (keyboard.RIGHT, keyboard.DOWN): (-SPEED, BACKWARD_RIGHT),

    (keyboard.UP, keyboard.LEFT): (SPEED, FORWARD_LEFT),
    (keyboard.LEFT, keyboard.UP): (SPEED, FORWARD_LEFT),
    (keyboard.DOWN, keyboard.LEFT): (-SPEED, BACKWARD_LEFT),
    (keyboard.LEFT, keyboard.DOWN): (-SPEED, BACKWARD_RIGHT)
}


def set_vel_and_steer(speed_angle):
    ego_vehicle.setCruisingSpeed(speed_angle[0])
    ego_vehicle.setSteeringAngle(speed_angle[1])


def main():
    while ego_vehicle.step() != -1:
        try:
            set_vel_and_steer(SIGNALS[(keyboard.getKey(), keyboard.getKey())])
        except KeyError:
            pass


if __name__ == '__main__':
    main()
