'''
Project logger, camera logging using global variable
'''

from datetime import date
import time
import cv2
from pathlib import Path
from from_root import from_root, from_here
import csv

from datetime import datetime


Path("images_log").mkdir(parents=True, exist_ok=True)
fields = ['Timestamp', 'Connected', 'NotConnected']
camera_dict = [{'Timestamp': None, 'Connected': [], 'NotConnected': []} ]
num_of_cameras = 3
updates = 0

def update_camera_status():
    with open('camera_status.csv', 'a', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        # writer.writeheader()
        writer.writerows(camera_dict)

def camera_status_log(cam_id, status):
    global camera_dict
    global updates
    if status:
        camera_dict[0]['Connected'].append(cam_id)
    else:
        camera_dict[0]['NotConnected'].append(cam_id)
    updates += 1
    if updates == num_of_cameras:
        camera_dict[0]['Timestamp'] = datetime.utcnow()
        update_camera_status()
        camera_dict[0]['Connected'] = []
        camera_dict[0]['NotConnected'] = []
        updates = 0




'''
demo


import logger
import cv2
import time
import numpy as np

logger.camera_status_log(1, True)
logger.camera_status_log(3, False)
logger.camera_status_log(4, True)

time.sleep(1)
logger.camera_status_log(2, True)
logger.camera_status_log(5, True)
logger.camera_status_log(6, True)

time.sleep(1)
logger.camera_status_log(1, True)
logger.camera_status_log(7, False)
logger.camera_status_log(8, True)

time.sleep(1)
logger.camera_status_log(1, False)
logger.camera_status_log(7, False)

'''