# Robotic Leader Follower Capstone Project
Wayne State University Senior Capstone Project to develop a semi-autonomous robotic vehicle.

## Preparing a Raspberry Pi For Leader/Follower
### Setting Up SSH
1. Connect the Pi to a monitor and power source
2. The default username is "pi" and the default password is "raspberry"
3. sudo raspi-config
4. Network configuration
5. Change the Raspberry Pi's name to something more specific.
   * This will be referred to as $PI_NAME in step 9.
6. Enter the WiFi SSID.
7. Enter the WiFi password.
8. Select Interfacing Options
9. Enable SSH
10. Reboot
11. On another computer, open a terminal and enter: ssh pi@$PI_NAME
12. Enter the password.

### Setup Repository After SSH
1. sudo apt-get update
2. sudo apt-get upgrade
3. sudo apt-get install bluez
4. sudo apt-get install xboxdrv
5. sudo raspi-config
6. Select Interfacing Options
7. Enable Camera
8. Enable I2C
9. Save changes
10. git clone --recurse-submodules https://github.com/johnshamoon/robotic-leader-follower.git
11. cd SunFounder_PiCar-V
12. sudo ./install_dependencies
13. picar servo-install
    * Adjust wheel and camera servos during this step.
14. export LD_LIBRARY_PATH=/usr/local/lib/ >> .bashrc

### Connect Bluetooth Controller
1. echo "sudo bash -c echo 1 > /sys/module/bluetooth/parameters/disable_ertm" >> .bashrc 
2. sudo bluetoothctl
3. power on
4. agent on
5. default-agent
6. scan on
7. pair $ADDRESS
8. trust $ADDRESS
9. connect $ADDRESS
10. quit
11. ls /dev/input/js0
    * This should exist if the controller paired and connected properly.

### Compiling and Installing OpenCV
Installing OpenCV on Raspbian requires compiling it yourself. Here's are the steps to compile and link OpenCV to Python:
1. sudo apt-get update
2. sudo apt-get upgrade
3. sudo apt-get install -y build-essential cmake pkg-config
4. sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
5. sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
6. sudo apt-get install -y libxvidcore-dev libx264-dev
7. sudo apt-get install -y libgtk2.0-dev
8. sudo apt-get install -y libatlas-base-dev gfortran
9. sudo apt-get install -y python2.7-dev python3-dev
10. cd ~
11. git clone https://github.com/opencv/opencv.git
12. git clone https://github.com/opencv/opencv_contrib.git
13. pip install numpy
14. cd ~/opencv
15. mkdir build
16. cd build
17. cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON ..
18. make -j1
    * Using more jobs will cause compilation to fail.
    * This will likely require more virtual (swap) memory. View that section for instructions.
19. sudo make install
20. sudo ldconfig

### Adding Virtual Memory
Compiling OpenCV will most likely require more RAM than the Pi has. We can solve this by adding more virtual (swap) memory. Here are the steps to do that:
1. free -m
   * This command can show you if the system has any swap memory configured. If this says 0, continue to the next steps.
2. df -h
   * This command shows you the amount of storage you are currently using. Decide how much space you can sacrifice for virtual memory.
3. sudo fallocate -l 4G /swapfile
   * This allocates 4GB to the swapfile. Decide what number is best for you. 4 should be plenty to compile OpenCV.
4. ls -lh /swapfile
   * Verify that the file was created with the correct amount of memory.
5. sudo chmod 600 /swapfile
6. sudo mkswap /swapfile
7. sudo swapon /s
8. free -m
   * Verify that the swapfile has been turned on.
9. Our swapfile changes will reset when the Pi reboots. Add the following line in /etc/fstab to make these change permanent:
   * /swapfile none swap sw 0 0
