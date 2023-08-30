'''
Project logger
'''

import logger
import cv2
import time
import numpy as np


# Load the image
# image = cv2.imread("cat.png")

image = cv2.imread("Rgb.jpg")

print( image.dtype.metadata )

# logger.log_image(image, "Color", "23452346246")


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

'''