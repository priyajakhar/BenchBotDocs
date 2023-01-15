#!/usr/bin/env python3
import cv2
import depthai as dai
import time
# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
cam = pipeline.create(dai.node.ColorCamera)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
#cam.setIspScale(3,9)

#cam.setVideoSize(1080,720)
cam.setVideoSize(800,500)
#cam.setPreviewSize(500,500)
cam.setFps(1)

# XLinkOut
xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName('feed')
cam.isp.link(xout.input)

xin = pipeline.create(dai.node.XLinkIn)
xin.setStreamName('control')
xin.out.link(cam.inputControl)

# [1000, 800, 625, 500, 400, 313]
ISO = [100, 125, 160, 200, 250, 320, 400, 500, 640, 800, 1000, 1250, 1600]
SS = [313, 400, 500, 625, 800, 1000]
ctrl = dai.CameraControl()
#SS[ss]


def adjust_exposure(img, i, s):
    #print(img.shape)
    Y = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    a, b = len(Y[Y<25]), len(Y[Y>230])
    x, y = a/(a+b), b/(a+b)
    #print(f"Pixels:\t\t{a}\t\t{b}")
    #print(f"Pixels:\t\t{x}\t\t{y}")

    if( abs(x-y) > 0.5 ):
        if(x>y):
            if s == len(SS)-1:
                i = min(i+1, 12)
            else:
                s = min(s+1, 5)
        else:
            if i == 0:
                s = max(0, s-1)
            else:
                i = max(0, i-1)
    

    #ctrl.setManualExposure(SS[s], ISO[i])
    ctrl.setManualExposure(30000, ISO[i])
    print(SS[s], ISO[i])
    #iso = min(iso+1, 12)
    cmd.send(ctrl)
    return i, s


# Connect to device with pipeline
with dai.Device(pipeline) as device:
    #device.setLogLevel(dai.LogLevel.INFO)
    #device.setLogOutputLevel(dai.LogLevel.INFO)
    feed = device.getOutputQueue("feed")
    cmd = device.getInputQueue(name="control")

    iso = 6
    ss = 5
    ctrl.setAutoFocusLensRange(129, 145)
    #iso = min(iso+1, 12)
    cmd.send(ctrl)

    stamp = time.time()

    while True:
        img = feed.get().getCvFrame()
        im = cv2.resize(img, (406,304), interpolation = cv2.INTER_AREA)
        cv2.imshow('CAM_FEED', im)

        #img = feed.tryGet()
        #if img is not None:
            #   cv2.imshow('CAM_FEED', img.getCvFrame())

        if( time.time()-stamp > 2 ):
            iso, ss = adjust_exposure(im, iso, ss)
            stamp = time.time()

        if cv2.waitKey(1) == ord('q'):
            break
