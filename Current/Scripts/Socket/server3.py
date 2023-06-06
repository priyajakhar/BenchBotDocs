import argparse
import time
import math
from pathlib import Path
import cv2
import depthai as dai
from csv import writer
import numpy as np
from datetime import date
import queue


# Start defining a pipeline
pipeline = dai.Pipeline()


monoRight = pipeline.create(dai.node.MonoCamera)
xoutRight = pipeline.create(dai.node.XLinkOut)
xoutRight.setStreamName("right")
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)


monoLeft = pipeline.create(dai.node.MonoCamera)
xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutLeft.setStreamName("left")
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)


# depth
Depth = pipeline.create(dai.node.StereoDepth)
Depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
Depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
Depth.setLeftRightCheck(True)
Depth.setExtendedDisparity(True)
Depth.setSubpixel(False)
Depth.setNumFramesPool(2)


xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("disparity")
monoRight.out.link(Depth.right)
monoLeft.out.link(Depth.left)
#Depth.disparity.link(xoutDepth.input)
Depth.depth.link(xoutDepth.input)




# Connect to device with pipeline
with dai.Device(pipeline) as device:
   qDepth = device.getOutputQueue(name="disparity", maxSize=2, blocking=False)
  
   init_dsp = (255 / Depth.initialConfig.getMaxDisparity())
   print(Depth.initialConfig.getMaxDisparity(), init_dsp)


   n = 20


   with open('data.csv', 'a', newline='') as f_object:
       writer_object = writer(f_object)
       for i in range(n):
          
           t = str(time.time())
           inDepth = None
           while inDepth is None:  inDepth = qDepth.tryGet()
           dframeo = inDepth.getFrame()
           #print(np.shape(dframeo), dframeo[5:10, 5:10])
           dframe = (dframeo * init_dsp).astype(np.uint8)
           cv2.imwrite(f"depth/{t}_Depth.png", dframeo)
           writer_object.writerow( [np.amax(dframeo)] )
      
       f_object.close()