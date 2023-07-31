"""
    running the nn model with iso adjustment logic
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

import math
import queue

today = str(date.today())
dirName = "images_"+today
Path(dirName).mkdir(parents=True, exist_ok=True)

__blob_path = '\model.blob'
nn_shape = (1024,1024)
nn_path = os.path.join(os.getcwd() + __blob_path)
pipeline = dai.Pipeline()
pipeline.setOpenVINOVersion(version=dai.OpenVINO.VERSION_2021_4)
        
RGB_Node = pipeline.createColorCamera()
RGB_Node.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
RGB_Node.setBoardSocket(dai.CameraBoardSocket.RGB)
RGB_Node.setVideoSize(2048,2048)
RGB_Node.setPreviewSize(1024,1024)
RGB_Node.setInterleaved(False)

# script = pipeline.createScript()
# RGB_Node.preview.link(script.inputs['isp_in'])
# script.inputs['isp_in'].setBlocking(False)
# script.inputs['isp_in'].setQueueSize(10)

# script.setScript("""
    # import time
    # while True:
        # frame = node.io['isp_in'].get()
        # num = frame.getSequenceNum()
        # if (num%5) == 0:
            # node.io['isp_out'].send(frame)
        # time.sleep(0.08)
# """)

# videoEnc = pipeline.create(dai.node.VideoEncoder)
# videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
# RGB_Node.video.link(videoEnc.input)

RGB_Out = pipeline.create(dai.node.XLinkOut)
RGB_Out.setStreamName("rgb")
RGB_Node.video.link(RGB_Out.input)
# RGB_Out.setFpsLimit(1)
# RGB_Out.input.setBlocking(False)
# RGB_Out.input.setQueueSize(1)
# videoEnc.bitstream.link(RGB_Out.input)

nn_node = pipeline.create(dai.node.NeuralNetwork)
nn_node.setBlobPath(nn_path)
nn_node.input.setBlocking(False)
nn_node.input.setQueueSize(1)
RGB_Node.preview.link(nn_node.input)
# script.outputs['isp_out'].link(nn_node.input)

seg_out = pipeline.create(dai.node.XLinkOut)
seg_out.setStreamName("seg out")
nn_node.out.link(seg_out.input)

monoRight = pipeline.create(dai.node.MonoCamera)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
xoutRight = pipeline.create(dai.node.XLinkOut)
xoutRight.setStreamName("right")

monoLeft = pipeline.create(dai.node.MonoCamera)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutLeft.setStreamName("left")

monoRight.out.link(xoutRight.input)
monoLeft.out.link(xoutLeft.input)

# scriptr = pipeline.createScript()
# scriptr.inputs['inr'].setQueueSize(10)
# monoRight.out.link(scriptr.inputs['inr'])
# scriptr.setScript("""
    # import time
    # while True:
        # frame = node.io['inr'].get()
        # num = frame.getSequenceNum()
        # if (num%5) == 0:
            # node.io['framer'].send(frame)
        # time.sleep(0.08)
# """)
# scriptr.outputs['framer'].link(xoutRight.input)

# scriptl = pipeline.createScript()
# scriptl.inputs['inl'].setQueueSize(10)
# monoLeft.out.link(scriptl.inputs['inl'])
# scriptl.setScript("""
    # import time
    # while True:
        # frame = node.io['inl'].get()
        # num = frame.getSequenceNum()
        # if (num%5) == 0:
            # node.io['framel'].send(frame)
        # time.sleep(0.08)
# """)
# scriptl.outputs['framel'].link(xoutLeft.input)

fps = 6
RGB_Node.setFps(fps)
monoRight.setFps(fps)
monoLeft.setFps(fps)
RGB_Node.setIsp3aFps(1)
monoRight.setIsp3aFps(1)
monoLeft.setIsp3aFps(1)

Depth = pipeline.create(dai.node.StereoDepth)
Depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
Depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
Depth.setLeftRightCheck(True)
Depth.setExtendedDisparity(False)
Depth.setSubpixel(False)

xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("depth")
monoRight.out.link(Depth.right)
monoLeft.out.link(Depth.left)
Depth.depth.link(xoutDepth.input)

xin1 = pipeline.create(dai.node.XLinkIn)
xin1.setNumFrames(1)   
xin1.setMaxDataSize(1) 
xin1.setStreamName("controlr") 
xin1.out.link(RGB_Node.inputControl) 
 
xin2 = pipeline.create(dai.node.XLinkIn)   
xin2.setNumFrames(1)
xin2.setMaxDataSize(1) 
xin2.setStreamName("controlm") 
xin2.out.link(monoLeft.inputControl)   
xin2.out.link(monoRight.inputControl)

''' 
    iso adjustment code
'''
nISO = 19
ISO = np.logspace(1.25, 2, num=nISO+1, endpoint=True, base=40, dtype=int)
SS = [313, 400, 500, 625, 800, 1000]
T = 15
B = 12
dT = 1.99
nQ = 4
w = np.flip(np.logspace(1, 0, num=nQ, endpoint=True))


def setisoss(fi, fs, col):
    ctr1 = dai.CameraControl()
    ctr1.setManualExposure(SS[fs], ISO[fi])
    if col:
        qControl1.send(ctr1)
    else:
        qControl2.send(ctr1)

def add_frame(img, col):
    if col:
        im = cv2.resize(img, (406,304), interpolation = cv2.INTER_AREA)
        Y = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([Y],[0],None,[32],[0,256])
        if( cor_grp.qsize()>=nQ ): cor_grp.get(0)
        cor_grp.put(hist)
    else:
        Y = cv2.resize(img, (320,180), interpolation = cv2.INTER_AREA)
        hist = cv2.calcHist([Y],[0],None,[32],[0,256])
        if( mono_grp.qsize()>=nQ ): mono_grp.get(0)
        mono_grp.put(hist)

def adjust_exposure(i, s, col):
    frm = []
    if col:
        for p in range(cor_grp.qsize()):    frm.append(w[p]*cor_grp.queue[p])
    else:
        for p in range(mono_grp.qsize()):    frm.append(w[p]*mono_grp.queue[p])
    arr = np.array(frm)
    
    summ = arr.sum(axis=0)
    peak = np.max(summ)
    pos = np.where(summ == peak)[0][0]

    if pos not in range(B, T): # 104 to 128 range by default
        # increase iso or ss
        if( pos < B):
            if s == len(SS)-1:
                i = min(i+1, nISO)
            else:
                s = min(s+1, 5)
        else:
            if i == 0:
                s = max(0, s-1)
            else:
                i = max(0, i-1)
    if col: setisoss(i, s, True)
    else:   setisoss(i, s, False)
    return i, s



with dai.Device(pipeline) as device:
    # device.setLogLevel(dai.LogLevel.INFO)
    # device.setLogOutputLevel(dai.LogLevel.INFO)
    
    segmentation_queue = device.getOutputQueue("seg out",10,False)
    rgb_queue = device.getOutputQueue("rgb",2,False)
    qDepth = device.getOutputQueue(name="depth", maxSize=2, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=2, blocking=False)
    qLeft = device.getOutputQueue(name="left", maxSize=2, blocking=False)
    qControl1 = device.getInputQueue(name="controlr")  
    qControl2 = device.getInputQueue(name="controlm")

    iso, ss = 6, 5
    miso, mss = 0, 5
    cor_grp = queue.Queue(nQ)
    mono_grp = queue.Queue(nQ)
    
    for z in range(10):
        # print(z)
        # c, r, l = rgb_queue.get(), qRight.get(), qLeft.get()
        c = rgb_queue.get()
    print("first loop")
    for z in range(10):
        # print(z)
        r = qRight.get()
        c = rgb_queue.get()
        
        # img = cv2.imdecode(c.getData(), cv2.IMREAD_COLOR)
        img = c.getCvFrame()
        # img = c.getFrame()
        add_frame(img, True)
        add_frame(r.getFrame(), False)
        iso, ss = adjust_exposure(iso, ss, True)
        miso, mss = adjust_exposure(miso, mss, False)
    print("second loop")

    sgdiffs = np.array([])
    stamp = time.time()
    start = time.time()
    
    for i in range(50):
        last = dai.Clock.now()
        t = str(time.time())
        
        rgb_data = rgb_queue.get()
        inRight = qRight.get()
        inLeft = qLeft.get()
        inDepth = qDepth.get()
        # print("\nfetched")
        im = Image.fromarray(inDepth.getFrame())
        im.save(f"{dirName}/{t}_Depth.png")
        
        segmentation_labels = None
        while segmentation_labels is None:  segmentation_labels = segmentation_queue.tryGet()
        seg_labels = np.array(segmentation_labels.getFirstLayerFp16()).reshape(128,128)
        cv2.imwrite(f"{dirName}/{t}_Seg.jpg", seg_labels)
        
        
        # rgb_img = cv2.imdecode(rgb_data.getData(), cv2.IMREAD_COLOR)
        rgb_img = rgb_data.getCvFrame()
        add_frame(rgb_img, True)
        add_frame(inRight.getFrame(), False)
            
        if( time.time()-stamp > dT ):
            iso, ss = adjust_exposure(iso, ss, True)
            miso, mss = adjust_exposure(miso, mss, False)
            stamp = time.time()
            
        time.sleep(0.35)
        latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
        sgdiffs = np.append(sgdiffs, latencyMs)
        
        
        # print(latencyMs)
        
        
        
    print("Done in ", time.time()-start)
    print(sgdiffs)