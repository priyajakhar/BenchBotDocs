import depthai as dai
from multiprocessing import Process
import cv2
from pathlib import Path
import time
import numpy as np

stop_p = False
# This can be customized to pass multiple parameters
def startcollection(cam_id, cam_no):
    print('Started', cam_no)
    # Start defining a pipeline
    pipeline = dai.Pipeline()

    # Define a source - color camera
    cam_rgb = pipeline.create(dai.node.ColorCamera)
    cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
    cam_rgb.setInterleaved(False)
    cam_rgb.initialControl.setSharpness(0)     # range: 0..4, default: 1		
    cam_rgb.initialControl.setLumaDenoise(0)   # range: 0..4, default: 1		
    cam_rgb.initialControl.setChromaDenoise(4) # range: 0..4, default: 1

    monoRight = pipeline.create(dai.node.MonoCamera)
    monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

    monoLeft = pipeline.create(dai.node.MonoCamera)
    monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
    monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

    Depth = pipeline.create(dai.node.StereoDepth)
    Depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
    Depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
    Depth.setLeftRightCheck(True)
    Depth.setExtendedDisparity(False)
    Depth.setSubpixel(False)
    monoRight.out.link(Depth.right)
    monoLeft.out.link(Depth.left)

    # Create output
    xout_rgb = pipeline.create(dai.node.XLinkOut)
    xout_rgb.setStreamName("rgb")
    cam_rgb.isp.link(xout_rgb.input)

    xoutRight = pipeline.create(dai.node.XLinkOut)
    xoutRight.setStreamName("right")
    monoRight.out.link(xoutRight.input)

    xoutLeft = pipeline.create(dai.node.XLinkOut)
    xoutLeft.setStreamName("left")
    monoLeft.out.link(xoutLeft.input)

    xoutDepth = pipeline.create(dai.node.XLinkOut)
    xoutDepth.setStreamName("disparity")
    Depth.disparity.link(xoutDepth.input)
    init_disp = Depth.initialConfig.getMaxDisparity()

    print('Working till', cam_no)

    # device = dai.Device(pipeline)
    cam = dai.DeviceInfo(cam_id) # MXID
    device = dai.Device(pipeline, cam)
    print('Broke', cam_no)

    device.setLogLevel(dai.LogLevel.INFO)
    device.setLogOutputLevel(dai.LogLevel.INFO)

    qRGB = device.getOutputQueue(name="rgb", maxSize=1, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=1, blocking=False)
    qLeft = device.getOutputQueue(name="left", maxSize=1, blocking=False)
    qDepth = device.getOutputQueue(name="disparity", maxSize=1, blocking=False)

    for r in range(20):
        inRgb = qRGB.get()
        # inRgb, inRight = qRGB.get(), qRight.get()

    i = 0
    n = 5

    while(i<n):
        print('Running', cam_no)
        t = time.time()
        inRgb = qRGB.get()
        cv2.imwrite(f"{dirName}/{cam_no}_{t}_Rgb.png", inRgb.getCvFrame())
        inRight = qRight.get()
        cv2.imwrite(f"{dirName}/{cam_no}_{t}_Right.png", inRight.getFrame())
        inLeft = qLeft.get()
        cv2.imwrite(f"{dirName}/{cam_no}_{t}_Left.png", inLeft.getFrame())
        inDepth = qDepth.get()
        dframe = inDepth.getFrame()
        dframe = (dframe * (255 / init_disp)).astype(np.uint8)
        cv2.imwrite(f"{dirName}/{cam_no}_{t}_Depth.png", dframe)

        i += 1
    
    global stop_p
    stop_p = True
    print('I am done', cam_no)


dirName = "oak_images"
Path(dirName).mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    
    device_infos = dai.Device.getAllAvailableDevices()
    print("Found", len(device_infos), "devices")

    idx = 1
    for dev in device_infos:
        # print(type(dev.getMxId()))
        cam = dev.getMxId()
        p = Process(target=startcollection, args=(cam, idx))
        p.start()
        p.join
        if(stop_p):
            break
        idx += 1

    print('Devices closed')