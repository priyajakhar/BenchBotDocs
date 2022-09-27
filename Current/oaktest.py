from pathlib import Path
import cv2
import depthai as dai
import time
import numpy as np

########################### OAK-D Funcs ###########################
colordirName = "color_data"
dirName = "mono_data"

def dirsetup():
    Path(dirName).mkdir(parents=True, exist_ok=True)
    Path(colordirName).mkdir(parents=True, exist_ok=True)

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
monoRight = pipeline.create(dai.node.MonoCamera)
xoutRight = pipeline.create(dai.node.XLinkOut)

monoLeft = pipeline.create(dai.node.MonoCamera)
xoutLeft = pipeline.create(dai.node.XLinkOut)

camRgb = pipeline.create(dai.node.ColorCamera)
# camRgb.setPreviewSize(3840, 2160)
xoutRgb = pipeline.create(dai.node.XLinkOut)

Depth = pipeline.create(dai.node.StereoDepth)
xoutDepth = pipeline.create(dai.node.XLinkOut)

xoutRight.setStreamName("right")
xoutLeft.setStreamName("left")
xoutRgb.setStreamName("rgb")
xoutDepth.setStreamName("disparity")


xin = pipeline.create(dai.node.XLinkIn)
xin.setStreamName("control")

videoEnc = pipeline.create(dai.node.VideoEncoder)
videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)

xoutStill = pipeline.create(dai.node.XLinkOut)
xoutStill.setStreamName("still")




# Properties
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

Depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
Depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
Depth.setLeftRightCheck(True)
Depth.setExtendedDisparity(False)
Depth.setSubpixel(False)

# Linking
monoRight.out.link(xoutRight.input)
monoLeft.out.link(xoutLeft.input)
camRgb.preview.link(xoutRgb.input)

monoRight.out.link(Depth.right)
monoLeft.out.link(Depth.left)
Depth.disparity.link(xoutDepth.input)



camRgb.video.link(xoutRgb.input)
xin.out.link(camRgb.inputControl)
camRgb.still.link(videoEnc.input)
videoEnc.bitstream.link(xoutStill.input)





# Device setup
device = dai.Device(pipeline)

qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)
qLeft = device.getOutputQueue(name="left", maxSize=4, blocking=False)
qRGB = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
qDepth = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)


qStill = device.getOutputQueue(name="still", maxSize=4, blocking=True)
qControl = device.getInputQueue(name="control")

def flushframes(n):
    for i in range(n):
        inRight = qRight.get()
        inLeft = qLeft.get()
        inRgb = qRGB.get()
        inDepth = qDepth.get()


dirsetup()
flushframes(50)


def captureImage():
    #   flushframes(20)
    inRgb = qRGB.get()
    t = str(int(time.time()))

    ctrl = dai.CameraControl()
    ctrl.setCaptureStill(True)
    qControl.send(ctrl)

    inRight = qRight.get()
    inLeft = qLeft.get()
    
    inDepth = qDepth.get()
    dframe = inDepth.getFrame()
    dframe = (dframe * (255 / Depth.initialConfig.getMaxDisparity())).astype(np.uint8)

    cv2.imwrite(f"{dirName}/Right_{t}.png", inRight.getFrame())
    cv2.imwrite(f"{dirName}/Left_{t}.png", inLeft.getFrame())
    cv2.imwrite(f"{dirName}/Depth_{t}.png", dframe)
    #   cv2.imwrite(f"{colordirName}/Rgb_{t}.png", inRgb.getCvFrame())

    if qStill.has():
        stillframe = qStill.get().getData()
        stillframe = qStill.get().getFrame()
        cv2.imwrite(f"{colordirName}/Rgb_{t}.png", stillframe)

###################################################################


# Capture Images
for i in range(2):
    print('Clicking picture....')
    time.sleep(2)
    captureImage()
