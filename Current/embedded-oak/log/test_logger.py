'''
Project logger
'''

import logger
import cv2
import time
import numpy as np


'''
    reading contents of csv file
'''
# import csv
# import sys
# cam_log = 'camera_log/camera_status.csv'
# img_log = 'images_log/images_log.csv'
# with open(img_log) as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     for row in csv_reader:
#         print(row)
# sys.exit()


'''
    reading contents of json file
'''
# import json
# import sys
# f = open('camera_log/Camera_1.json')
# data = json.load(f)
# print(data)
# f.close()
# sys.exit()


'''
    testing image log function
'''
# Latitude : 35.773713
# Longitude: -78.672968
# Easting: 710325.92
# Northing: 3961357.01
# zone: 17S

# Load the image
# image = cv2.imread("cat.png")
image = cv2.imread("Rgb.jpg")

# print( image.dtype.metadata )

logger.log_image(image, "Color", [35.773713, -78.672968])


# def convert_ddtodms(dd_gps):
#     lat = 45.543210
# >>> deg = int(dd_gps)
# >>> min = int((dd_gps-deg)*60)
# >>> sec = ((dd_gps-deg)*60) - min
# >>> print(deg, min, sec)

# def make_image(self, img_data, gps_data):
    
#     picSaveName = picNameTimeString + ".jpg"
#     print("save image ")
#     picPath = os.path.join(output_dir, picSaveName)
#     cv2.imwrite(picPath, cv_img, params)

#     picGpsTimeFlt =self.rostime2floatSecs(gps_data.header.stamp)
#     gpsTimeString = datetime.utcfromtimestamp(picGpsTimeFlt).strftime('%Y:%m:%d %H:%M:%S')
#     self.set_gps_location(picPath, lat ...





'''
    testing camera log function
'''

# logger.camera_status_log(1, True)
# logger.camera_status_log(3, False)
# logger.camera_status_log(4, True)

# time.sleep(1)
# logger.camera_status_log(2, True)
# logger.camera_status_log(5, True)
# logger.camera_status_log(6, True)

# time.sleep(1)
# logger.camera_status_log(1, True)
# logger.camera_status_log(7, False)
# logger.camera_status_log(8, True)

# time.sleep(1)
# logger.camera_status_log(1, False)
# logger.camera_status_log(7, False)


# logger.camera_status_log(1, 'Connected')
# logger.camera_status_log(2, 'Connected')
# logger.camera_status_log(3, 'NotConnected')
# logger.camera_status_log(4, 'Connected')
# logger.camera_status_log(5, 'Connected')
# logger.camera_status_log(6, 'NotConnected')
# logger.camera_status_log(7, 'NotConnected')
# logger.camera_status_log(8, 'Connected')
# logger.system_camera_status()

'''
35 46 25.3668
78 40 22.6848
'''