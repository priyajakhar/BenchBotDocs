''' script to demonstrate use of OAK_Camera class objects '''

from OAK_Camera import Camera
import time
import sys
from datetime import date
import cv2
from pathlib import Path
import keyboard


# today = str(date.today())
# dirName = "images_"+today
# Path(dirName).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # initialize camera object
    camera = Camera("169.254.54.191")
    # upload pipeline to the camera and start running it

    camera.run()
    timeout_start = time.time()
    timeout = 10
    while not camera.camera_ready() and time.time() < ( timeout_start + timeout ):
        time.sleep(1)
    if not camera.camera_ready():
        print("\nError: Couldn't connect to device!")
        sys.exit()
    
    time.sleep(3)
    st = time.time()
    with open('backyard_data.txt', 'a') as f:
        # while time.time()-st < 120:
        while True:
            angles = camera.get_imu_reading()
            f.write(f"{angles[0]}\t{angles[1]}\t{angles[2]}\n")
            time.sleep(0.25)
            if keyboard.is_pressed("q"):
                break

    camera.stop_camera()
