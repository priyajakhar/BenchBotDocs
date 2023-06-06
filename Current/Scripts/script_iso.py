#!/usr/bin/env python3
import cv2
import depthai as dai

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
cam = pipeline.create(dai.node.ColorCamera)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setIspScale(2,3)
cam.setVideoSize(720,720)
cam.setPreviewSize(500,500)

# Script node
script = pipeline.create(dai.node.Script)
#cam.preview.link(script.inputs['rgb'])

script.setScript("""
    import time

    ISO = [100, 125, 160, 200, 250, 320, 400, 500, 640, 800, 1000, 1250, 1600]
    SS = [1000, 800, 625, 500, 400, 313]
    iso = 0
    ss = 3
    ctrl = CameraControl()

    i = 0
    while i<13:
        ctrl.setManualExposure(30000, ISO[iso]) 
        node.io['out'].send(ctrl)
        #node.warn(f"Before: {i}")
        time.sleep(1)
        #node.warn(f"After: {i}")
        iso = iso+1
        i = i+1
    node.warn("Done")
""")
script.outputs['out'].link(cam.inputControl)


# XLinkOut
xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName('video')
cam.video.link(xout.input)


# Connect to device with pipeline
with dai.Device(pipeline) as device:
    #device.setLogLevel(dai.LogLevel.INFO)
    #device.setLogOutputLevel(dai.LogLevel.INFO)
    feed = device.getOutputQueue("video")
    while True:
        img = feed.get()
        cv2.imshow('CAM_FEED', img.getCvFrame())

        #img = feed.tryGet()
        #if img is not None:
         #   cv2.imshow('CAM_FEED', img.getCvFrame())
        if cv2.waitKey(1) == ord('q'):
            break