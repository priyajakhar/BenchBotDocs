"""
    running the nn model (works in current pipeline formation)
"""

#!/usr/bin/env python3

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

__blob_path = '\models\longer.blob'
nn_shape = (1024,1024)
nn_path = os.path.join(os.getcwd() + __blob_path)
# print(nn_path)
pipeline = dai.Pipeline()
pipeline.setOpenVINOVersion(version=dai.OpenVINO.VERSION_2021_4)
        
RGB_Node = pipeline.createColorCamera()
RGB_Node.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
RGB_Node.setBoardSocket(dai.CameraBoardSocket.RGB)
RGB_Node.setVideoSize(2048,2048)
RGB_Node.setPreviewSize(1024,1024)
RGB_Node.setInterleaved(False)

RGB_Out = pipeline.create(dai.node.XLinkOut)
RGB_Out.setStreamName("rgb")
RGB_Node.video.link(RGB_Out.input)

nn_node = pipeline.create(dai.node.NeuralNetwork)
nn_node.setBlobPath(nn_path)
nn_node.input.setBlocking(False)
nn_node.input.setQueueSize(1)
# nn_node.setNumInferenceThreads(1) # By default 2 threads are used
# nn_node.setNumNCEPerInferenceThread(1) # By default, 1 NCE is used per thread

RGB_Node.preview.link(nn_node.input)

seg_out = pipeline.create(dai.node.XLinkOut)
seg_out.setStreamName("seg out")
nn_node.out.link(seg_out.input)

monoRight = pipeline.create(dai.node.MonoCamera)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

xoutRight = pipeline.create(dai.node.XLinkOut)
xoutRight.setStreamName("right")
monoRight.out.link(xoutRight.input)

monoLeft = pipeline.create(dai.node.MonoCamera)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutLeft.setStreamName("left")
monoLeft.out.link(xoutLeft.input)

# works till 7 fps when using script node
# works till 8 fps when script node is not used
RGB_Node.setFps(5)
monoRight.setFps(5)
monoLeft.setFps(5)
RGB_Node.setIsp3aFps(1)
monoRight.setIsp3aFps(1)
monoLeft.setIsp3aFps(1)

Depth = pipeline.create(dai.node.StereoDepth)
Depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
Depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
Depth.setLeftRightCheck(True)
Depth.setExtendedDisparity(False)
Depth.setSubpixel(False)
# Depth.setNumFramesPool(2)

xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("depth")
monoRight.out.link(Depth.right)
monoLeft.out.link(Depth.left)
Depth.depth.link(xoutDepth.input)


with dai.Device(pipeline) as device:
    # device.setLogLevel(dai.LogLevel.INFO)
    # device.setLogOutputLevel(dai.LogLevel.INFO)
    
    segmentation_queue = device.getOutputQueue("seg out",2,False)
    rgb_queue = device.getOutputQueue("rgb",2,False)
    qDepth = device.getOutputQueue(name="depth", maxSize=2, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=2, blocking=False)
    qLeft = device.getOutputQueue(name="left", maxSize=2, blocking=False)
   
    start = time.time()
    sgdiffs = []
    n = 10
    
    for i in range(n):
        last = dai.Clock.now()
        t = str(time.time())
        inDepth = qDepth.get()
        
        rgb_data = rgb_queue.get()
        # rgb_data = rgb_queue.tryGet()
        if rgb_data is not None:
            rgb_img = rgb_data.getCvFrame()
            # rgb_img = cv2.imdecode(rgb_data.getData(), cv2.IMREAD_COLOR)
            cv2.imwrite(f"{dirName}/{t}_Rgb.jpg", rgb_img)
        
        segmentation_labels = segmentation_queue.get()
        # original model
        # seg_labels = np.array(segmentation_labels.getFirstLayerFp16()).reshape(128,128)
        # longer model
        seg_labels = np.array(segmentation_labels.getFirstLayerFp16()).reshape(64,64)
        # shorter model
        # print(len(segmentation_labels.getFirstLayerInt32()))
        # seg_labels = np.array(segmentation_labels.getFirstLayerInt32()).reshape(1024,1024)
        cv2.imwrite(f"{dirName}/{t}_Seg.jpg", seg_labels)
        
        inRight = qRight.get()
        inLeft = qLeft.get()
        
        # cv2.imwrite(f"{dirName}/{t}_Right.png", inRight.getFrame())
        # cv2.imwrite(f"{dirName}/{t}_Left.png", inLeft.getFrame())
        im = Image.fromarray(inDepth.getFrame())
        im.save(f"{dirName}/{t}_Depth.png")
        latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
        sgdiffs = np.append(sgdiffs, latencyMs)
        
    print("Average Time: ", (time.time()-start)/n)
    # print(sgdiffs)
    
# with open('full_latency_shorter.txt', 'w') as f:
    # for it in sgdiffs:
        # f.write(str(it))
        # f.write('\n')