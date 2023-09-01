#!/usr/bin/env python3

import time
import depthai as dai
import cv2
import threading
import os, sys
import numpy as np

# create pipeline
pipeline = dai.Pipeline()
nodes = dict()
disparity = False
monoout = False
fps = 5

''' ColorCamera (RGB) node '''
camRgb = pipeline.createColorCamera()
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
# camRgb.setVideoSize(2048,2048)
camRgb.setPreviewSize(1024,1024)
# camRgb.setIspScale(1280,800)

# camRgb.setPreviewSize(600, 400)
camRgb.setInterleaved(False)

# manip1 = pipeline.create(dai.node.ImageManip)
# manip1.initialConfig.setResize(1280,800)
# manip1.setMaxOutputFrameSize(1280*800*3)
# camRgb.isp.link(manip1.inputImage)

xoutRgb = pipeline.create(dai.node.XLinkOut)
xoutRgb.setStreamName("rgb")
nodes.update({'rgb': None})
camRgb.preview.link(xoutRgb.input)
# manip1.out.link(xoutRgb.input)


            
''' Right Left MonoCamera node '''     
monoRight = pipeline.create(dai.node.MonoCamera)
monoRight.setBoardSocket(dai.CameraBoardSocket.CAM_C)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

monoLeft = pipeline.create(dai.node.MonoCamera)
monoLeft.setBoardSocket(dai.CameraBoardSocket.CAM_B)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

if monoout:
    xoutRight = pipeline.create(dai.node.XLinkOut)
    xoutRight.setStreamName("right")
    monoRight.out.link(xoutRight.input)
    nodes.update({'right': None})

    xoutLeft = pipeline.create(dai.node.XLinkOut)
    xoutLeft.setStreamName("left")
    monoLeft.out.link(xoutLeft.input)
    nodes.update({'left': None})


camRgb.setFps(fps)    
monoRight.setFps(fps)
monoLeft.setFps(fps)

''' StereoDepth node '''
Depth = pipeline.create(dai.node.StereoDepth)
Depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
Depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
Depth.setLeftRightCheck(True)
Depth.setExtendedDisparity(False)
Depth.setSubpixel(False)

xoutDepth = pipeline.create(dai.node.XLinkOut)
monoRight.out.link(Depth.right)
monoLeft.out.link(Depth.left)
if disparity:
    Depth.disparity.link(xoutDepth.input)
    xoutDepth.setStreamName("disparity")
    nodes.update({'disparity': None})
else:
    Depth.depth.link(xoutDepth.input)
    xoutDepth.setStreamName("depth")
    nodes.update({'depth': None})



queues = []
with dai.Device(pipeline) as device:

    # initializing the queue
    for idx, node_name in enumerate(nodes):
        queues.append( device.getOutputQueue(node_name, 5, False) )

    for i in range(20):
        for idx, node_name in enumerate(nodes):
            nodes[node_name] = queues[idx].get()
    
    strt = time.time()
    
    while time.time()-strt < 3:
        t =  time.time()
        
        # fetch frames from all queues
        for idx, node_name in enumerate(nodes):
            nodes[node_name] = queues[idx].get()

        rgb_frame = nodes['rgb'].getCvFrame()
        # rgb_frame2 = nodes['rgb'].getFrame()
        # rgb_frame3 = nodes['rgb'].getData()
        
        
        f_out = nodes['depth'].getFrame()
        
        print( sys.getsizeof(rgb_frame), sys.getsizeof(rgb_frame2), sys.getsizeof(rgb_frame3) )
        
        r_out = nodes['right'].getCvFrame()
        l_out = nodes['left'].getCvFrame()

        print( sys.getsizeof(r_out), sys.getsizeof(l_out), sys.getsizeof(f_out) )
        
        
        # cv2.imshow("rgb", rgb_frame)
        # if cv2.waitKey(1) == ord('q'):
            # break

        # cv2.imwrite(f"{t}_Rgb.jpg", rgb_frame)
        # cv2.imwrite(f"{t}_Depth.jpg", f_out)



'''
RGB
1024*1024*3 = 3145728
3145872 .getFrame() = 144 .getData() = 112
diff = 144

2048*2048*3 = 12582912
12583056 .getFrame() = 128 .getData() = 112
diff = 144

Mono, Depth
.getFrame() = 128 128 128
1280*800 = 1024000
1024128
diff = 128


'''