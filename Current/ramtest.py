import time
import cv2
import depthai as dai
import numpy as np

## Create pipeline
pipeline = dai.Pipeline()

cams = []
cams.append('rgb')
cams.append('left')
cams.append('right')
cams.append('stereo')


# raw, isp, preview, video, still
if 'rgb' in cams:
    # color camera
    camRgb = pipeline.create(dai.node.ColorCamera)
    camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
    # camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

    # camRgb.setIspScale(16,17)
    # camRgb.setIspScale(2,3)
    # camRgb.setIspNumFramesPool(1)
    # sensorCenterCrop()
    
    # Set number of frames in all pools
    # camRgb.setNumFramesPool(1,1,1,1,1)
    # camRgb.setNumFramesPool(2,2,2,2,2)
    camRgb.setNumFramesPool(2,2,0,0,1)
    # camRgb.setNumFramesPool(3,3,3,3,3)
    # camRgb.setSensorCrop(0.5, 0)
    # print(camRgb.getSensorCrop())

    xoutRgb = pipeline.create(dai.node.XLinkOut)
    xoutRgb.setStreamName("rgb")
    camRgb.isp.link(xoutRgb.input)

    # print(camRgb.getRawNumFramesPool(), camRgb.getIspNumFramesPool(), camRgb.getPreviewNumFramesPool(), camRgb.getVideoNumFramesPool(), camRgb.getStillNumFramesPool())
    # print(camRgb.getIspSize(), camRgb.getStillSize(), camRgb.getPreviewSize(), camRgb.getVideoSize())

if 'left' in cams:
    monoLeft = pipeline.create(dai.node.MonoCamera)
    monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
    monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

    # setting and getting not working on this oak-d
    monoLeft.setNumFramesPool(1)
    monoLeft.setRawNumFramesPool(1)
    # print("Left camera stats: ", monoLeft.getRawNumFramesPool(), monoLeft.getNumFramesPool())
    # print(monoLeft.getResolutionSize())

    xoutLeft = pipeline.create(dai.node.XLinkOut)
    xoutLeft.setStreamName("left")
    monoLeft.out.link(xoutLeft.input)

if 'right' in cams:
    monoRight = pipeline.create(dai.node.MonoCamera)
    monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

    monoRight.setNumFramesPool(1)
    monoRight.setRawNumFramesPool(1)
    # print("Right camera stats: ", monoRight.getRawNumFramesPool(), monoRight.getNumFramesPool())

    xoutRight = pipeline.create(dai.node.XLinkOut)
    xoutRight.setStreamName("right")
    monoRight.out.link(xoutRight.input)

if 'stereo' in cams:
    Depth = pipeline.create(dai.node.StereoDepth)
    Depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
    Depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
    Depth.setLeftRightCheck(True)
    Depth.setExtendedDisparity(False)
    Depth.setSubpixel(False)
    init_dsp = (255 / Depth.initialConfig.getMaxDisparity())
    Depth.setNumFramesPool(1)
    xoutDepth = pipeline.create(dai.node.XLinkOut)
    xoutDepth.setStreamName("disparity")
    monoRight.out.link(Depth.right)
    monoLeft.out.link(Depth.left)
    Depth.disparity.link(xoutDepth.input)

# video encoder
videoEnc = pipeline.create(dai.node.VideoEncoder)
videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
videoEnc.setNumFramesPool(1)
camRgb.still.link(videoEnc.input)

xoutStill = pipeline.create(dai.node.XLinkOut)
xoutStill.setStreamName("cap_img")
videoEnc.bitstream.link(xoutStill.input)

# videoEnc.setFrameRate(1)
# # print(videoEnc.getNumFramesPool())


# Script node
script = pipeline.create(dai.node.Script)
script.setScript("""
    import time
    ctrl = CameraControl()
    ctrl.setCaptureStill(True)
    while True:
        time.sleep(0.5)
        node.io['out'].send(ctrl)
""")
script.outputs['out'].link(camRgb.inputControl)


# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    device.setLogLevel(dai.LogLevel.INFO)
    device.setLogOutputLevel(dai.LogLevel.INFO)

    #device.setLogLevel(dai.LogLevel.DEBUG)
    #device.setLogOutputLevel(dai.LogLevel.DEBUG)
    #DEPTHAI_LEVEL=info python test.py


    # DDR: 115.25 / 340.93 MiB
    # bootloader
    # (res, info) = dai.DeviceBootloader.getFirstAvailableDevice()
    # if res == True:
    #     print(f'Found device with name: {info.name}')
    #     bl = dai.DeviceBootloader(device)
    #     print(f'Version: {bl.getVersion()}')

    qRGB = device.getOutputQueue(name="rgb", maxSize=5, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=5, blocking=False)
    qLeft = device.getOutputQueue(name="left", maxSize=5, blocking=False)
    qDepth = device.getOutputQueue(name="disparity", maxSize=5, blocking=False)
    qStill = device.getOutputQueue(name="cap_img", maxSize=5, blocking=False)

    # video = device.getOutputQueue(name="video")

    print("\n\nStarted\n\n")
    start = time.time()
    # run for 3 seconds
    while( time.time()-start < 5 ):
        t = str(time.time())
        # v = video.tryGet()

        inRgb = qRGB.tryGet()
        if inRgb is not None:
            frame = inRgb.getCvFrame()
            cv2.imshow("rgb", frame)
        
        inRight = qRight.tryGet()
        if inRight is not None:
            frame = inRight.getFrame()
            cv2.imshow("right", frame)
        
        inLeft = qLeft.tryGet()
        if inLeft is not None:
            frame = inLeft.getFrame()
            cv2.imshow("left", frame)
        
        inDepth = qDepth.tryGet()
        if inDepth is not None:
            dframe = inDepth.getFrame()
            dframe = (dframe * init_dsp).astype(np.uint8)
            cv2.imshow("depth", dframe)

        if qStill.has():
            fName = f"{int(time.time() * 1000)}.png"
            with open(fName, "wb") as f:
                f.write(qStill.get().getData())
                print('\nImage saved to', fName)

print("\nDone\n")
