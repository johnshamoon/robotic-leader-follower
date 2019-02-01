from controller import Keyboard

from vehicle import Driver

driver = Driver()
timestep = int(driver.getBasicTimeStep())

speed = 0.5
MAX_SPEED = 1.8
angle = 0

SENSOR_MAX = 1000

front_left_distance_sensor = driver.getDistanceSensor('front_left_sensor')
front_center_distance_sensor = driver.getDistanceSensor('front_center_sensor')
front_right_distance_sensor = driver.getDistanceSensor('front_right_sensor')
front_left_distance_sensor.enable(timestep)
front_center_distance_sensor.enable(timestep)
front_right_distance_sensor.enable(timestep)

while driver.step() != -1:
  left_val = front_left_distance_sensor.getValue()
  center_val = front_center_distance_sensor.getValue()
  right_val = front_right_distance_sensor.getValue()

  if center_val > 1 and center_val < SENSOR_MAX:
    print("center", center_val)
    angle += 160
  elif left_val > 1 and left_val < SENSOR_MAX:
    print("left", left_val)
    angle += 160
  elif right_val > 1 and right_val < SENSOR_MAX:
    print("right", right_val)
    angle += 160
  else:
    angle = 0

  if speed > MAX_SPEED:
    speed = MAX_SPEED
  if angle > 0.5:
    angle = 0.5

  driver.setSteeringAngle(angle)
  driver.setCruisingSpeed(speed)