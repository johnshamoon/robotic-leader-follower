# Robotic Leader Follower Capstone Project
Wayne State University Senior Capstone Project to develop a semi-autonomous robotic vehicle.

## Preparing a Raspberry Pi For Leader/Follower
### Setting Up SSH
1. Connect the Pi to a monitor and power source.
2. The default username is "pi" and the default password is "raspberry"
3. Enter the Raspberry Pi configuration tool.
> ```shell
> sudo raspi-config
> ```
4. Network Configuration.
5. Change the Raspberry Pi's name to something more specific.
   * This will be referred to as $PI_NAME in later steps.
6. Enter the WiFi SSID.
7. Enter the WiFi password.
8. Select Interfacing Options.
9. Enable SSH.
10. Reboot.
11. On another computer, open a terminal and enter:
> ```shell
> ssh pi@$PI_NAME
> ```
12. Enter the password.

### Setup Repository After SSH
1. Update package lists.
> ```shell
> sudo apt-get update
> ```
2. Update installed packages.
> ```shell
> sudo apt-get upgrade
> ```
3. Install the Bluez Bluetooth stack.
> ```shell
> sudo apt-get install bluez
> ```
4. Install the XBox gamepad driver.
> ```shell
> sudo apt-get install xboxdrv
> ```
5. Enter the Raspberry Pi configuration tool.
> ```shell
> sudo raspi-config
> ```
6. Select Interfacing Options.
7. Enable Camera.
8. Enable I2C.
9. Save changes.
10. Clone the repository and submodules.
> ```console
> git clone --recurse-submodules https://github.com/johnshamoon/robotic-leader-follower.git
> ```
11. Enter the SunFounder submodule.
> ```shell
> cd SunFounder_PiCar-V
> ```
12. Install the SunFounder dependencies.
> ```shell
> sudo ./install_dependencies
> ```
13. Adjust wheel and camera servos.
> ```shell
> picar servo-install
> ```
14. Add libraries path to bashrc.
> ```shell
> export LD_LIBRARY_PATH=/usr/local/lib/ >> ~/.bashrc
> ```

### Connect Bluetooth Controller
1. Disable ERTM on startup.
> ```shell
> echo "sudo su -s /bin/bash -c \"echo 1 > /sys/module/bluetooth/parameters/disable_ertm\"" >> .bashrc
> ```
2. Enter the Bluetooth command line control tool.
> ```shell
> sudo bluetoothctl
> ```
3. Power on the Bluetooth controller.
> ```shell
> power on
> ```
4. Enable the Bluetooth agent.
> ```shell
> agent on
> ```
5. Set the current agent as the default.
> ```shell
> default-agent
> ```
6. Scan for devices.
> ```shell
> scan on
> ```
7. Pair to the Bluetooth controller's Bluetooth address.
> ```shell
> pair $ADDRESS
> ```
8. Trust the Bluetooth controller.
> ```shell
> trust $ADDRESS
> ```
9. Connect to the Bluetooth controller.
> ```shell
> connect $ADDRESS
> ```
10. Exit bluetoothctl.
> ```shell
> quit
> ```
11. Check that the controller paired and connected properly.
> ```shell
> ls /dev/input/js0
> ```

### Compiling and Installing OpenCV
Installing OpenCV on Raspbian requires manual compilation. Here's are the steps to compile and link OpenCV to Python:
1. Update package lists.
> ```shell
> sudo apt-get update
> ```
2. Update installed packages.
> ```shell
> sudo apt-get upgrade
> ```
3. Install necessary libraries and packages.
> ```shell
> sudo apt-get install -y build-essential cmake pkg-config
> sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
> sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
> sudo apt-get install -y libxvidcore-dev libx264-dev
> sudo apt-get install -y libgtk2.0-dev
> sudo apt-get install -y libatlas-base-dev gfortran
> sudo apt-get install -y python2.7-dev python3-dev
> ```
4. Go back to the home directory.
> ```shell
> cd ~
> ```
5. Clone the OpenCV source.
> ```shell
> git clone https://github.com/opencv/opencv.git
> ```
6. Clone OpenCV's extra modules.
> ```
> git clone https://github.com/opencv/opencv_contrib.git
> ```
7. Install numpy.
> ```shell
> pip install numpy
> ```
8. Enter the opencv directory.
> ```shell
> cd ~/opencv
> ```
9. Create a directory called build.
> ```shell
> mkdir build
> ```
10. Enter the build directory.
> ```shell
> cd build
> ```
11. Configure the project and create the cmake cache entries.
> ```shell
> cmake -D CMAKE_BUILD_TYPE=RELEASE \
>     -D CMAKE_INSTALL_PREFIX=/usr/local \
>     -D INSTALL_PYTHON_EXAMPLES=ON \
>     -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
>     -D BUILD_EXAMPLES=ON ..
> ```
12. Build OpenCV.
    * Using more jobs will cause compilation to fail.
    * This will likely require more virtual (swap) memory. View [Adding Virtual Memory](#adding-virtual-memory) for instructions.
> ```shell
> make -j1
> ```
13. Install OpenCV.
> ```shell
> sudo make install
> ```
14. Link the newly installed OpenCV libraries.
> ```shell
> sudo ldconfig
> ```

### Adding Virtual Memory
Compiling OpenCV will most likely require more RAM than the Pi has. This can be solved by adding more virtual (swap) memory. Here are the steps to do that:
1. Check if the system has any swap memory configured.
> ```shell
> free -m
> ```
2. Check how much storage the system has and how much can be sacrificed for virtual memory.
> ```shell
> df -h
> ```
3. Allocate some memory to a swapfile. 4GB should be plenty.
> ```shell
> sudo fallocate -l 4G /swapfile
> ```
4. Verify that the file was created with the correct amount of memory.
> ```shell
> ls -lh /swapfile
> ```
5. Change the permissions on swapfile.
> ```shell
> sudo chmod 600 /swapfile
> ```
6. Make swapfile an actual swap-file.
> ```shell
> sudo mkswap /swapfile
> ```
7. Enable the swap-file.
> ```shell
> sudo swapon /swapfile
> ```
8. Verify that the swap-file has been turned on.
> ```shell
> free -m
> ```
9. Our swapfile changes will reset when the Pi reboots. Add the following line in /etc/fstab to make these change permanent:
> ```shell
> /swapfile none swap sw 0 0
> ```

### Python Dependencies
This system uses Python 2.7 as is required by the SunFounder APIs.
The following packages are required:
> numpy>=1.15.1
