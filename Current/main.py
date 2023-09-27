import argparse
import time
import math
from pathlib import Path
from PIL import Image
import cv2
import depthai as dai
from csv import writer
import numpy as np
from datetime import date
import queue
 
today = str(date.today())
dirName = "images_"+today
def dirsetup():
   Path(dirName).mkdir(parents=True, exist_ok=True)

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
camRgb.initialControl.setSharpness(0)     # range: 0..4, default: 1    
camRgb.initialControl.setLumaDenoise(0)   # range: 0..4, default: 1    
camRgb.initialControl.setChromaDenoise(4) # range: 0..4, default: 1

# modifying isp frame and then feeding it to encoder
manip = pipeline.create(dai.node.ImageManip)
manip.initialConfig.setCropRect(0.006, 0, 1, 1)
manip.setNumFramesPool(2)
manip.setMaxOutputFrameSize(18385920)
manip.initialConfig.setFrameType(dai.ImgFrame.Type.NV12)
camRgb.isp.link(manip.inputImage)

videoEnc = pipeline.create(dai.node.VideoEncoder)
videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
manip.out.link(videoEnc.input)

xoutRgb = pipeline.create(dai.node.XLinkOut)
xoutRgb.setStreamName("rgb")
videoEnc.bitstream.link(xoutRgb.input)


monoRight = pipeline.create(dai.node.MonoCamera)
xoutRight = pipeline.create(dai.node.XLinkOut)
xoutRight.setStreamName("right")
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

monoLeft = pipeline.create(dai.node.MonoCamera)
xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutLeft.setStreamName("left")
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

scriptr = pipeline.createScript()
monoRight.out.link(scriptr.inputs['inr'])
scriptr.setScript("""
    import time
    while True:
        frame = node.io['inr'].get()
        num = frame.getSequenceNum()
        if (num%10) == 0:
            node.io['framer'].send(frame)
        time.sleep(0.09)
""")
scriptr.outputs['framer'].link(xoutRight.input)

scriptl = pipeline.createScript()
monoLeft.out.link(scriptl.inputs['inl'])
scriptl.setScript("""
    import time
    while True:
        frame = node.io['inl'].get()
        num = frame.getSequenceNum()
        if (num%10) == 0:
            node.io['framel'].send(frame)
        time.sleep(0.09)
""")
scriptl.outputs['framel'].link(xoutLeft.input)

camRgb.setFps(10)
monoRight.setFps(10)
monoLeft.setFps(10)

camRgb.setIsp3aFps(1)
monoRight.setIsp3aFps(1)
monoLeft.setIsp3aFps(1)

# depth
Depth = pipeline.create(dai.node.StereoDepth)
Depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
Depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
Depth.setLeftRightCheck(True)
Depth.setExtendedDisparity(False)
Depth.setSubpixel(True)
# Depth.setNumFramesPool(2)

xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("disparity")
monoRight.out.link(Depth.right)
monoLeft.out.link(Depth.left)
Depth.depth.link(xoutDepth.input)


# Connect to device with pipeline
with dai.Device(pipeline) as device:
    device.setLogLevel(dai.LogLevel.INFO)
    device.setLogOutputLevel(dai.LogLevel.INFO)

    qRGB = device.getOutputQueue("rgb", maxSize=2, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=2, blocking=False)
    qLeft = device.getOutputQueue(name="left", maxSize=2, blocking=False)
    qDepth = device.getOutputQueue(name="disparity", maxSize=2, blocking=False)

    stamp = time.time()
    start = time.time()
    
    for z in range(20):
        c, r, l, d = qRGB.get(), qRight.get(), qLeft.get(), qDepth.get()
    for z in range(10):
        c, r, l, d = qRGB.get(), qRight.get(), qLeft.get(), qDepth.get()
        img = cv2.imdecode(c.getData(), cv2.IMREAD_COLOR)
        add_frame(img, True)
        add_frame(r.getFrame(), False)
        iso, ss = adjust_exposure(iso, ss, True)
        miso, mss = adjust_exposure(miso, mss, False)

    with open('data.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        for i in range(n):
            
            t = str(time.time())
            
            strt = dai.Clock.now()
            
            last = dai.Clock.now()
            inRgb, inLeft, inRight, inDepth = None, None, None, None
            while inRgb is None:    inRgb = qRGB.tryGet()
            while inRight is None:  inRight = qRight.tryGet()
            while inLeft is None:   inLeft = qLeft.tryGet()
            while inDepth is None:  inDepth = qDepth.tryGet()
            latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
            fdiffs = np.append(fdiffs, latencyMs)

            last = dai.Clock.now()
            # img = cv2.imdecode(inRgb.getData(), cv2.IMREAD_COLOR)
            # cv2.imwrite(f"{dirName}/{t}_Rgb_{ISO[iso]}.jpg", img)
            # cv2.imwrite(f"{dirName}/{t}_Right_{ISO[miso]}.png", inRight.getFrame())
            # cv2.imwrite(f"{dirName}/{t}_Left.png", inLeft.getFrame())
            # im = Image.fromarray(inDepth.getFrame())
            # im.save(f"{dirName}/{t}_Depth.png")
            latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
            sdiffs = np.append(sdiffs, latencyMs)
            # dframe = inDepth.getFrame()
            # dframe = (dframe * init_dsp).astype(np.uint8)
            # cv2.imwrite(f"{dirName}/{t}_Depth.png", dframe)

            last = dai.Clock.now()
            add_frame(img, True)
            add_frame(inRight.getFrame(), False)
            latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
            fadiffs = np.append(fadiffs, latencyMs)

            if( time.time()-stamp > dT ):
                last = dai.Clock.now()
                iso, ss = adjust_exposure(iso, ss, True)
                latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
                adjdiffs = np.append(adjdiffs, latencyMs)
                
                last = dai.Clock.now()
                miso, mss = adjust_exposure(miso, mss, False)
                latencyMs = (dai.Clock.now() - last).total_seconds() * 1000
                ddiffs = np.append(ddiffs, latencyMs)
                stamp = time.time()
                # writer_object.writerow( [ISO[iso], SS[ss], ISO[miso], SS[mss]] )
                
            latencyMs = (dai.Clock.now() - strt).total_seconds() * 1000
            fullloop = np.append(fullloop, latencyMs)
        
        f_object.close()