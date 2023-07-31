"""
    running the nn model
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

__blob_path = '\model.blob'
nn_shape = (1024,1024)
nn_path = os.path.join(os.getcwd() + __blob_path)
#print(nn_path)
pipeline = dai.Pipeline()
pipeline.setOpenVINOVersion(version=dai.OpenVINO.VERSION_2021_4)
        
RGB_Node = pipeline.createColorCamera()
RGB_Node.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
RGB_Node.setBoardSocket(dai.CameraBoardSocket.RGB)
# RGB_Node.setIspScale(1,2)
RGB_Node.setVideoSize(2048,2048)
RGB_Node.setPreviewSize(1024,1024)
RGB_Node.setInterleaved(False)

# script = pipeline.createScript()
# RGB_Node.preview.link(script.inputs['isp_in'])
# script.inputs['isp_in'].setBlocking(False)
# script.inputs['isp_in'].setQueueSize(5)

# script.setScript("""
    # import time
    # while True:
        # frame = node.io['isp_in'].get()
        # num = frame.getSequenceNum()
        # if (num%2) == 0:
            # node.io['isp_out'].send(frame)
        # time.sleep(0.09)
# """)

# videoEnc = pipeline.create(dai.node.VideoEncoder)
# videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
# RGB_Node.video.link(videoEnc.input)
# script.outputs['isp_out'].link(videoEnc.input)

RGB_Out = pipeline.create(dai.node.XLinkOut)
RGB_Out.setStreamName("rgb")
# RGB_Out.input.setBlocking(False)
# RGB_Out.input.setQueueSize(1)
# videoEnc.bitstream.link(RGB_Out.input)
# script.outputs['isp_out'].link(RGB_Out.input)
RGB_Node.video.link(RGB_Out.input)

nn_node = pipeline.create(dai.node.NeuralNetwork)
nn_node.setBlobPath(nn_path)
nn_node.input.setBlocking(False)
nn_node.input.setQueueSize(1)
RGB_Node.preview.link(nn_node.input)
# script.outputs['isp_out'].link(nn_node.input)

seg_out = pipeline.create(dai.node.XLinkOut)
seg_out.setStreamName("seg out")
nn_node.out.link(seg_out.input)

'''
    Depth output related code
'''

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
RGB_Node.setFps(8)
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

'''
'''

with dai.Device(pipeline) as device:
    device.setLogLevel(dai.LogLevel.INFO)
    device.setLogOutputLevel(dai.LogLevel.INFO)

    diffs = np.array([])
    segmentation_queue = device.getOutputQueue("seg out",2,False)
    rgb_queue = device.getOutputQueue("rgb",1,False)
    qDepth = device.getOutputQueue(name="depth", maxSize=1, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=2, blocking=False)
    qLeft = device.getOutputQueue(name="left", maxSize=2, blocking=False)
    
    
    # for i in range(10):
        # segmentation_labels = segmentation_queue.get()
        # rgb_data = rgb_queue.get()
        # last = dai.Clock.now()

    rdiffs = []
    sgdiffs = []
    srdiffs = []
    ssdiffs = []
    ddiffs = []
    # diffs = []
    
    start = time.time()
    
    for i in range(10):
        t = str(time.time())
        
        last = dai.Clock.now()
        rgb_data = rgb_queue.tryGet()
        if rgb_data is not None:
            rgb_img = rgb_data.getCvFrame()
            # rgb_img = rgb_data.getData()
            # rgb_img = cv2.imdecode(rgb_data.getData(), cv2.IMREAD_COLOR)
            cv2.imwrite(f"{dirName}/{t}_Rgb.jpg", rgb_img)
            # pass
        latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
        rdiffs = np.append(rdiffs, latencyMs)
        
        last = dai.Clock.now()
        segmentation_labels = segmentation_queue.get()
        latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
        sgdiffs = np.append(sgdiffs, latencyMs)
        last = dai.Clock.now()
        
        
        seg_labels = np.array(segmentation_labels.getFirstLayerFp16()).reshape(128,128)
        
        
        # latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
        # srdiffs = np.append(srdiffs, latencyMs)
        # last = dai.Clock.now()
        
        
        
        cv2.imwrite(f"{dirName}/{t}_Seg.jpg", seg_labels)
        
        
        # latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
        # ssdiffs = np.append(ssdiffs, latencyMs)
        # last = dai.Clock.now()
        
        
        
        inDepth = qDepth.get()
        im = Image.fromarray(inDepth.getFrame())
        im.save(f"{dirName}/{t}_Depth.png")
        
        
        inRight = qRight.get()
        inLeft = qLeft.get()
        inDepth = qDepth.get()
        # cv2.imwrite(f"{dirName}/{t}_Right.png", inRight.getFrame())
        # cv2.imwrite(f"{dirName}/{t}_Left.png", inLeft.getFrame())
        # im = Image.fromarray(inDepth.getFrame())
        # im.save(f"{dirName}/{t}_Depth.png")
        
        # print(len(segmentation_labels.getFirstLayerInt32()))
        # print(len(segmentation_labels.getFirstLayerFp16()))
        # segmentation_labels = np.array(segmentation_labels.getFirstLayerInt32()).reshape(nn_shape[0],nn_shape[1])

        # latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
        # ddiffs = np.append(ddiffs, latencyMs)
        # last = dai.Clock.now()
        
    print("Done in ", time.time()-start)
        
    with open('rgb_latency.txt', 'w') as f:
        for it in rdiffs:
            f.write(str(it))
            f.write('\n')
            
    with open('sg_latency.txt', 'w') as f:
        for it in sgdiffs:
            f.write(str(it))
            f.write('\n')
            
    # with open('sr_latency.txt', 'w') as f:
        # for it in srdiffs:
            # f.write(str(it))
            # f.write('\n')
            
    # with open('ss_latency.txt', 'w') as f:
        # for it in ssdiffs:
            # f.write(str(it))
            # f.write('\n')
            
    # with open('dd_latency.txt', 'w') as f:
        # for it in ddiffs:
            # f.write(str(it))
            # f.write('\n')
            
    
        

    # print(diffs)