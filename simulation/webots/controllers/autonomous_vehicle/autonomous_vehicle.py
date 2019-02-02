from controller import Keyboard
from vehicle import Driver

driver = Driver()
timestep = int(driver.getBasicTimeStep())

SPEED = 0.5
SENSOR_MAX = 1000
FRONT_LEFT_DISTANCE_SENSOR = driver.getDistanceSensor('front_left_sensor')
FRONT_CENTER_DISTANCE_SENSOR = driver.getDistanceSensor('front_center_sensor')
FRONT_RIGHT_DISTANCE_SENSOR = driver.getDistanceSensor('front_right_sensor')
FRONT_LEFT_DISTANCE_SENSOR.enable(timestep)
FRONT_CENTER_DISTANCE_SENSOR.enable(timestep)
FRONT_RIGHT_DISTANCE_SENSOR.enable(timestep)

angle = 0

while driver.step() != -1:
  left_val = FRONT_LEFT_DISTANCE_SENSOR.getValue()
  center_val = FRONT_CENTER_DISTANCE_SENSOR.getValue()
  right_val = FRONT_RIGHT_DISTANCE_SENSOR.getValue()

  if 1 < center_val < SENSOR_MAX:
    angle += 160
  elif 1 < left_val < SENSOR_MAX:
    angle += 160
  elif 1 < right_val < SENSOR_MAX:
    angle += 160
  else:
    angle = 0

  if angle > 0.5:
    angle = 0.5

  driver.setSteeringAngle(angle)
  driver.setCruisingSpeed(SPEED)