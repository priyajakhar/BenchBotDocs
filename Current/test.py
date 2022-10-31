from multiprocessing import Process, Pool
import threading
import argparse
import time
from pathlib import Path
import cv2
import depthai as dai
import numpy as np


dirName = "oak_images"
Path(dirName).mkdir(parents=True, exist_ok=True)


# arguments
argn = argparse.ArgumentParser()
argn.add_argument('-n', type=int, default=2)
argn.add_argument('-iso', type=int, default=400)
argn.add_argument('-fps', type=float, default=1)
argn.add_argument('-ss', type=float, default=16)
args = argn.parse_args()


# Create pipeline
pipeline = dai.Pipeline()


camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
camRgb.setInterleaved(False)
camRgb.initialControl.setSharpness(0)     # range: 0..4, default: 1		
camRgb.initialControl.setLumaDenoise(0)   # range: 0..4, default: 1		
camRgb.initialControl.setChromaDenoise(4) # range: 0..4, default: 1

xoutRgb = pipeline.create(dai.node.XLinkOut)
xoutRgb.setStreamName("rgb")
xoutRgb.input.setBlocking(False)
xoutRgb.input.setQueueSize(1)
camRgb.isp.link(xoutRgb.input)


# control pipeline
xin = pipeline.create(dai.node.XLinkIn)
xin.setMaxDataSize(1)
xin.setStreamName("control")
xin.out.link(camRgb.inputControl)


# Mono cameras
monoRight = pipeline.create(dai.node.MonoCamera)
xoutRight = pipeline.create(dai.node.XLinkOut)
xoutRight.setStreamName("right")
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
monoRight.out.link(xoutRight.input)


monoLeft = pipeline.create(dai.node.MonoCamera)
xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutLeft.setStreamName("left")
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
monoLeft.out.link(xoutLeft.input)


# depth
Depth = pipeline.create(dai.node.StereoDepth)
xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("disparity")
Depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
Depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
Depth.setLeftRightCheck(True)
Depth.setExtendedDisparity(False)
Depth.setSubpixel(False)
monoRight.out.link(Depth.right)
monoLeft.out.link(Depth.left)
Depth.disparity.link(xoutDepth.input)
init_dis = Depth.initialConfig.getMaxDisparity()

# queue definitions
device = dai.Device(pipeline)
qRight = device.getOutputQueue(name="right", maxSize=1, blocking=False)
qLeft = device.getOutputQueue(name="left", maxSize=1, blocking=False)
qRGB = device.getOutputQueue(name="rgb", maxSize=1, blocking=False)
qDepth = device.getOutputQueue(name="disparity", maxSize=1, blocking=False)
qControl = device.getInputQueue(name="control")


def manualExposure(expTimeMs, sensIso):
    # print("SS = " + str(expTimeMs)+" ISO = "+str(sensIso))
    expTimeUs = int(round(expTimeMs * 1000))
    ctrl = dai.CameraControl()
    ctrl.setManualExposure(expTimeUs, sensIso)
    qControl.send(ctrl)


def manualFocus(focus):
    ctrl = dai.CameraControl()
    ctrl.setManualFocus(focus)
    qControl.send(ctrl)


def set_fps_and_focus(fps):
    camRgb.setFps(fps)
    monoRight.setFps(fps)
    monoLeft.setFps(fps)


# image count
n = args.n
# iso and shutter speed
manualExposure(args.ss, args.iso)
# fps
set_fps_and_focus(args.fps)

# flushing starting frames
for r in range(30):
    inRgb = qRGB.get()
    inRight = qRight.get()
    inLeft = qLeft.get()
    inDepth = qDepth.get()



def show_feed(inRgb):
    j = 0
    while(j<1000):
        j += 1
        inRgb = qRGB.tryGet()
        if inRgb is not None:
            frame = inRgb.getCvFrame()
            frame = cv2.pyrDown(frame)
            frame = cv2.pyrDown(frame)
            cv2.imshow("Feed", frame)
        time.sleep(0.1)
        

def get_all(num):
    inRgb = qRGB.get()
    inRight = qRight.get()
    inLeft = qLeft.get()
    inDepth = qDepth.get()
    
    cv2.imwrite(f"{dirName}/{num}_Rgb.png", inRgb.getCvFrame())
    cv2.imwrite(f"{dirName}/{num}_Right.png", inRight.getFrame())
    cv2.imwrite(f"{dirName}/{num}_Left.png", inLeft.getFrame())
    dframe = inDepth.getFrame()
    dframe = (dframe * (255 / init_dis)).astype(np.uint8)
    cv2.imwrite(f"{dirName}/{num}_Depth.png", dframe)
        

def save_images(num, rgb, monor, monol, dep, disp):
    cv2.imwrite(f"{dirName}/{num}_Rgb.png", rgb)
    cv2.imwrite(f"{dirName}/{num}_Right.png", monor)
    cv2.imwrite(f"{dirName}/{num}_Left.png", monol)
    dframe = (dep * (255 / disp)).astype(np.uint8)
    cv2.imwrite(f"{dirName}/{num}_Depth.png", dframe)

if __name__ == '__main__':
    i = 0
    print("Started")
    start = time.time()

    #p = Process(target=show_feed, args=(qRGB,))
    #p.start()
    #p.join()

    #threading.Thread(target=show_feed).start()
        

    while(i<n):
        inRgb = qRGB.get()
        inRight = qRight.get()
        inLeft = qLeft.get()
        inDepth = qDepth.get()
        #threading.Thread(target=save_images, args=(i+1, inRgb.getCvFrame(), inRight.getFrame(), inLeft.getFrame(), inDepth.getFrame())).start()
        #time.sleep(1)
        
        p = Process(target=save_images, args=(i+1, inRgb.getCvFrame(), inRight.getFrame(), inLeft.getFrame(), inDepth.getFrame(), init_dis))
        p.start()
        p.join()
        time.sleep(1)
        i += 1
    
    print("Finished in", round(time.time()-start, 2))