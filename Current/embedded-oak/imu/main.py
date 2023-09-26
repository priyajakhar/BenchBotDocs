''' script to demonstrate use of OAK_Camera class objects '''

from imu import Camera
import time
import sys
from datetime import date
import cv2
from pathlib import Path


today = str(date.today())
dirName = "images_"+today
Path(dirName).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # initialize camera object
    camera = Camera("169.254.222.1")
    # upload pipeline to the camera and start running it
    camera.run()
    # wait for the camera to start up
    timeout_start = time.time()
    timeout = 10
    while not camera.camera_ready() and time.time() < ( timeout_start + timeout ):
        time.sleep(1)
    # if error in connecting to camera
    if not camera.camera_ready():
        print("\nError: Couldn't connect to device!")
        sys.exit()
    
    # fetch and save 5 rgb frames
    # for i in range(5):
        # t =  time.time()
        # frame = camera.get_image('rgb')
        # cv2.imwrite(f"{dirName}/{t}_Rgb.jpg", frame)

    time.sleep(5)
    # send "shut down" command for camera
    camera.stop_camera()