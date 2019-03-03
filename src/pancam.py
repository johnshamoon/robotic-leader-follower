from follower import Follower
import time

follower = Follower()

def seek():
    if follower.detect() == False:
        angle = follower._turn_angle + 45
        follower.turn_camera_left(angle)
        follower.stop()
    else:
        follower.reset_camera()
        follower.drive()

def main():
    while True:
        seek()

if __name__ == '__main__':
    main()