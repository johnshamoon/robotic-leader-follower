# AR Tag recognition with OpenCV 

### Installation 
You need to install a few modules to be able to generate tags or recognize them with a camera.

You can install these modules by running the following command in your console: 

>python -m pip install -r requirements.txt

### Usage
#### make_blob.py 
This script can be used to generate a new AR tag. It will be saved in the same directory as the script.

#### tag_recognition.py 
This script can be used to recognize a tag. It serves more as a "backend" script for recognizing ARTag objects. The script will print a 4x2 array to the console to signify the pixel location of each corner in the camera space.

#### tag_visualization.py 
This script can be used to visualize a tag. It does so by opening the webcam on your machine. Recognized tags should have a green border around them with a red dot on one corner to signify the current rotation of the tag. 

Recognized tags will also have a 3D Gizmo in the center of the tag. The red, green, and blue gizmos represent pitch, yaw, and roll respectively. 

In addition to the tag recognition, a live graph is also displayed to better visualize what's happening in the camera space. This will make it easier for us to see what's happening as we rotate and tilt the tag (to simulate vehicle movement).
