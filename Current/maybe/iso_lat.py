# "measuring latency for iso cmd to take effect on camera"

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
#pipeline.setXLinkChunkSize(0)

# Define a source - color camera
camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
# camRgb.setNumFramesPool(3,3,0,0,1)
camRgb.inputControl.setBlocking(False)
camRgb.inputControl.setQueueSize(1)
camRgb.setIspScale(1,3)
camRgb.setFps(1)

xoutRgb = pipeline.create(dai.node.XLinkOut)
xoutRgb.setStreamName("rgb")
camRgb.isp.link(xoutRgb.input)
xoutRgb.input.setBlocking(False)
xoutRgb.input.setQueueSize(2)

xin1 = pipeline.create(dai.node.XLinkIn)
xin1.setNumFrames(1)   
xin1.setMaxDataSize(1) 
xin1.setStreamName("controlr") 
xin1.out.link(camRgb.inputControl)


# Connect to device with pipeline
with dai.Device(pipeline) as device:
    qRGB = device.getOutputQueue("rgb", maxSize=2, blocking=False)
    qControl1 = device.getInputQueue(name="controlr")

    for z in range(20):
        c = qRGB.get()
    
    print(c.getSequenceNum())

    ctrl = dai.CameraControl()
    ctrl.setManualExposure(30000, 100)
    # print(time.time())
    t = time.time()
    qControl1.send(ctrl)

    last = dai.Clock.now()
    diffs = []

    for i in range(15):
        # t = str(time.time())
        inRgb = None
        while inRgb is None:    inRgb = qRGB.tryGet()
        # img = cv2.imdecode(inRgb.getData(), cv2.IMREAD_COLOR)
        # print(dai.Clock.now())
        if inRgb.getSensitivity() == 100:
            print(inRgb.getSequenceNum(), time.time()-t)
        latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
        diffs = np.append(diffs, latencyMs)
        last = dai.Clock.now()

    # print(diffs)
    time.sleep(1)