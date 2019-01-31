from vehicle import Driver
from controller import Keyboard
from numpy import pi

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

def set_vel_and_steer(v, s):
    ego_vehicle.setCruisingSpeed(v)
    ego_vehicle.setSteeringAngle(s)

def main():
    while ego_vehicle.step() != -1:
        key = keyboard.getKey()
        key_2 = keyboard.getKey()
        if key == keyboard.UP and key_2 == keyboard.LEFT:
            set_vel_and_steer(SPEED, FORWARD_LEFT)
        elif key == keyboard.UP and key_2 == keyboard.RIGHT:
            set_vel_and_steer(SPEED, FORWARD_RIGHT)
        elif key == keyboard.DOWN and key_2 == keyboard.LEFT:
            set_vel_and_steer(-SPEED, BACKWARD_LEFT)
        elif key == keyboard.DOWN and key_2 == keyboard.RIGHT:
            set_vel_and_steer(-SPEED, BACKWARD_RIGHT)
        elif key == keyboard.LEFT and key_2 == keyboard.UP:
            set_vel_and_steer(SPEED, LEFT)
        elif key == keyboard.RIGHT and key_2 == keyboard.UP:
            set_vel_and_steer(SPEED, RIGHT)
        elif key == keyboard.LEFT and key_2 == keyboard.DOWN:
            set_vel_and_steer(-SPEED, BACKWARD_LEFT)
        elif key == keyboard.RIGHT and key_2 == keyboard.DOWN:
            set_vel_and_steer(-SPEED, BACKWARD_RIGHT)
        elif key == keyboard.LEFT:
            set_vel_and_steer(NEUTRAL, LEFT)
        elif key == keyboard.RIGHT:
            set_vel_and_steer(NEUTRAL, RIGHT)
        elif key == keyboard.UP:
            set_vel_and_steer(SPEED, FORWARD)
        elif key == keyboard.DOWN:
            set_vel_and_steer(-SPEED, BACKWARD)
        else:
            set_vel_and_steer(NEUTRAL, NEUTRAL)

if __name__ == '__main__':
    main()
