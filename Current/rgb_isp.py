import threading
from multiprocessing import Process, Pool
import argparse
import time
from pathlib import Path
import cv2
import depthai as dai
import numpy as np

# global flag for stopping stream
stop_feed = False


dirName = "oak_images"
def dirsetup():
    Path(dirName).mkdir(parents=True, exist_ok=True)


# arguments
argn = argparse.ArgumentParser()
argn.add_argument('-n', type=int, default=20)
argn.add_argument('-iso', type=int, default=400)
argn.add_argument('-fps', type=float, default=1)
argn.add_argument('-ss', type=float, default=16)
args = argn.parse_args()


# Create pipeline
pipeline = dai.Pipeline()
# total available RAM is 358 MiB Mebibyte (MiB = 1.048576 MB)

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
# xoutRgb.setFpsLimit(5)


# control pipeline
xin = pipeline.create(dai.node.XLinkIn)
xin.setMaxDataSize(1) # can use small size since it's only control signals (40 to 1 now)
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


# Connect to device and start pipeline
with dai.Device(pipeline) as device:	
    i = 0
    # image count
    n = args.n
    # print("Taking "+ str(n)+" pictures")
    dirsetup()

    qRight = device.getOutputQueue(name="right", maxSize=1, blocking=False)
    qLeft = device.getOutputQueue(name="left", maxSize=1, blocking=False)
    qRGB = device.getOutputQueue(name="rgb", maxSize=1, blocking=False)
    qDepth = device.getOutputQueue(name="disparity", maxSize=1, blocking=False)
    qControl = device.getInputQueue(name="control")


    # iso and shutter speed
    manualExposure(args.ss, args.iso)
    # fps
    set_fps_and_focus(args.fps)

    for r in range(30):
        inRgb = qRGB.get()
        inRight = qRight.get()
        inLeft = qLeft.get()
        inDepth = qDepth.get()

    def save_images(num, rgb, monor, monol, dep):
        if(num==n):
            global stop_feed
            stop_feed = True
        cv2.imwrite(f"{dirName}/{num}_Rgb.png", rgb)
        cv2.imwrite(f"{dirName}/{num}_Right.png", monor)
        cv2.imwrite(f"{dirName}/{num}_Left.png", monol)
        dframe = (dep * (255 / Depth.initialConfig.getMaxDisparity())).astype(np.uint8)
        cv2.imwrite(f"{dirName}/{num}_Depth.png", dframe)
        

    def get_all(num):
        if(num==n):
            global stop_feed
            stop_feed = True
        print("I am thread",num)
        print("~~I am thread",num)
        cv2.imwrite(f"{dirName}/{num}_Rgb.png", inRgb.getCvFrame())
        cv2.imwrite(f"{dirName}/{num}_Right.png", inRight.getFrame())
        cv2.imwrite(f"{dirName}/{num}_Left.png", inLeft.getFrame())
        dframe = inDepth.getFrame()
        dframe = (dframe * (255 / Depth.initialConfig.getMaxDisparity())).astype(np.uint8)
        cv2.imwrite(f"{dirName}/{num}_Depth.png", dframe)
        


    def get_images(total):
        i = 0
        while(i<total):
            threading.Thread(target=get_all, args=(i+1,)).start()
            time.sleep(1)
            i += 1
    
    def show_feed():
        while not stop_feed:
            inRgb = qRGB.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise
            if inRgb is not None:
                frame = inRgb.getCvFrame()
                frame = cv2.pyrDown(frame)
                frame = cv2.pyrDown(frame)
                cv2.imshow("Feed", frame)


    print("Started")
    start = time.time()
    # last = start

    #threading.Thread(target=show_feed).start()
    # takes about 2 secs to save all 4 images

        #if u==15000:
            #last = time.time()
           # u = 0
            #threading.Thread(target=save_images, args=(i,)).start()
            #threading.Thread(target=get_all, args=(i+1,)).start()
           # time.sleep(0.5)
            
            #print("", round(time.time()-last, 2))
           # i += 1   
    #threading.Thread(target=get_images, args=(n,)).start()

    while(i<n):
        inRgb = qRGB.get()
        inRight = qRight.get()
        inLeft = qLeft.get()
        inDepth = qDepth.get()
        cv2.imwrite(f"{dirName}/{i}_Rgb.png", inRgb.getCvFrame())
        cv2.imwrite(f"{dirName}/{i}_Right.png", inRight.getFrame())
        cv2.imwrite(f"{dirName}/{i}_Left.png", inLeft.getFrame())
        dframe = inDepth.getFrame()
        dframe = (dframe * (255 / Depth.initialConfig.getMaxDisparity())).astype(np.uint8)
        cv2.imwrite(f"{dirName}/{i}_Depth.png", dframe)
        
        
        # threading.Thread(target=save_images, args=(i+1, inRgb.getCvFrame(), inRight.getFrame(), inLeft.getFrame(), inDepth.getFrame())).start()
        # time.sleep(1)
        i += 1
        # continue
        # inRgb = qRGB.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise
        # if inRgb is not None:
            # frame = inRgb.getCvFrame()
            # frame = cv2.pyrDown(frame)
            # frame = cv2.pyrDown(frame)
            # cv2.imshow("Feed", frame)
        



print("Finished in", round(time.time()-start, 2))
