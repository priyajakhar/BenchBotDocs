import time
from datetime import date
from pathlib import Path
from PIL import Image
import depthai as dai
import numpy as np
import cv2
import os, sys

today = str(date.today())
dirName = "images_"+today
Path(dirName).mkdir(parents=True, exist_ok=True)

pipeline = dai.Pipeline()
# 29995
# pipeline.setCameraTuningBlobPath('database_mono_AEtbl.bin')
# 8326
pipeline.setCameraTuningBlobPath('tuning_exp_limit_500us.bin')
# 495
        
monoRight = pipeline.create(dai.node.MonoCamera)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

monoLeft = pipeline.create(dai.node.MonoCamera)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutLeft.setStreamName("monos")
monoRight.out.link(xoutLeft.input)
monoLeft.out.link(xoutLeft.input)

with dai.Device(pipeline) as device:    
    m_queue = device.getOutputQueue("monos",30,False)
    
    for i in range(40):
        rgb_data = m_queue.get()
    
    for i in range(20):
        t = str(time.time())
        rgb_data = m_queue.get()
        print(rgb_data.getExposureTime(), rgb_data.getSensitivity())
        rgb_img = rgb_data.getFrame()
        cv2.imwrite(f"{dirName}/{t}_Mono.jpg", rgb_img)
        # rgb_data = rgb_queue.tryGet()
        # if rgb_data is not None:
            # print(rgb_data.getExposureTime())




























sys.exit()

RGB_Node = pipeline.createColorCamera()
RGB_Node.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
RGB_Node.setBoardSocket(dai.CameraBoardSocket.RGB)
RGB_Node.setVideoSize(2048,2048)
RGB_Node.setPreviewSize(1024,1024)
RGB_Node.setInterleaved(False)

RGB_Out = pipeline.create(dai.node.XLinkOut)
RGB_Out.setStreamName("rgb")
RGB_Node.video.link(RGB_Out.input)


with dai.Device(pipeline) as device:    
    rgb_queue = device.getOutputQueue("rgb",2,False)
    
    for i in range(20):
        t = str(time.time())
        rgb_data = rgb_queue.get()
        print(rgb_data.getExposureTime(), rgb_data.getSensitivity())
        rgb_img = rgb_data.getCvFrame()
        cv2.imwrite(f"{dirName}/{t}_Rgb.jpg", rgb_img)
        # rgb_data = rgb_queue.tryGet()
        # if rgb_data is not None:
            # print(rgb_data.getExposureTime())
