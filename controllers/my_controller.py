import math
from controller import Keyboard
from vehicle import Driver

driver = Driver()
timestep = int(driver.getBasicTimeStep())

keyboard = driver.getKeyboard()
keyboard.enable(timestep)

speed = 0
max_speed = 1.8
angle = 0
driver.setSteeringAngle(angle)
driver.setCruisingSpeed(speed)

sensor_max = 1000
front_left_sensor = driver.getDistanceSensor('front_left_sensor')
front_center_sensor = driver.getDistanceSensor('front_center_sensor')
front_right_sensor = driver.getDistanceSensor('front_right_sensor')
front_left_sensor.enable(timestep)
front_center_sensor.enable(timestep)
front_right_sensor.enable(timestep)

manualDrive = False

while driver.step() != -1:

  while True:
    key = keyboard.getKey()
    if key == -1:
      break
    if key == ord('m') or key == ord('M'):
      manualDrive = True
      print("Manual ENABLED")
      if not manualDrive: 
        manualDrive = True
    elif key == ord('a') or key == ord('A'):
      print("Manual DISABLED")
      manualDrive = False
      if manualDrive: 
        manualDrive = True

    if manualDrive:
      if key == keyboard.UP:
        if speed < 0:
          speed += 0.05
        else:
          speed += 0.005
      elif key == keyboard.DOWN:
        if speed > 0:
          speed -= 0.05
        else:
          speed -= 0.005
      elif key == keyboard.LEFT:
          angle -= 0.01
      elif key == keyboard.RIGHT:
          angle += 0.01
  
  if not manualDrive:
    left_val = front_left_sensor.getValue()
    center_val = front_center_sensor.getValue()
    right_val = front_right_sensor.getValue()

    if center_val > 400 and center_val < 600:
      speed -= (0.01 * speed)
    elif center_val > 600 and center_val < 800:
      speed /= 1.01

    if left_val > right_val:
      angle += (left_val - right_val) / (300 * sensor_max)
    elif right_val > left_val:
      angle -= (right_val - left_val) / (300 * sensor_max)
    else: 
      angle /= 0.2

    speed += 0.001

  if speed > max_speed:
    speed = max_speed
  if angle > 0.5:
    angle = 0.5
  elif angle < -0.5:
    angle = -0.5

  driver.setCruisingSpeed(speed)
  driver.setSteeringAngle(angle)

  pass
