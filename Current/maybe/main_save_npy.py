''' script to demonstrate use of OAK_Camera class objects '''

from OAK_Camera_Seg import Camera
import time
from datetime import date
import cv2
from pathlib import Path
import numpy as np
import sys


with open('seg.npy', 'rb') as f:
    a = np.load(f)
print(a.dtype, a.shape)
with open('depth.npy', 'rb') as f:
    a = np.load(f)
print(a.dtype, a.shape)
with open('rgb.npy', 'rb') as f:
    a = np.load(f)
print(a.dtype, a.shape)

sys.exit()

today = str(date.today())
dirName = "images_"+today
Path(dirName).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # initialize camera object
    camera = Camera()
    # upload pipeline to the camera and start running it
    camera.run()
    # time needed for the camera to start up
    time.sleep(5)
    
    # fetch and save 5 rgb frames
    for i in range(1):
        t =  time.time()

        frame = camera.get_seg()
        print(frame.dtype, frame.shape)
        with open('seg.npy', 'wb') as f:
            np.save(f, frame)
        frame = camera.get_depth()
        print(frame.dtype, frame.shape)
        with open('depth.npy', 'wb') as f:
            np.save(f, frame)
        frame = camera.get_rgb()
        print(frame.dtype, frame.shape)
        with open('rgb.npy', 'wb') as f:
            np.save(f, frame)
        cv2.imwrite(f"{dirName}/{t}_Rgb.jpg", frame)
        
    time.sleep(1)
    # send "shut down" command for camera
    camera.stop_camera()