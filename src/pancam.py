from follower import Follower
import time

follower = Follower()

def seek():
	tag_data = follower.detect()

	if tag_data == False:
		follower.stop()
	elif tag_data['x'] < 0:
		follower.turn_camera_left(1)
	elif tag_data['x'] > 0:
		follower.turn_camera_right(1)
	else:
		follower.reset_camera()

def main():
	while True:
		seek()

if __name__ == '__main__':
    main()	