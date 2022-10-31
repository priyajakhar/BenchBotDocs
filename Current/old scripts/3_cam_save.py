from pathlib import Path
import cv2
import depthai as dai
import time

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
monoRight = pipeline.create(dai.node.MonoCamera)
xoutRight = pipeline.create(dai.node.XLinkOut)

monoLeft = pipeline.create(dai.node.MonoCamera)
xoutLeft = pipeline.create(dai.node.XLinkOut)

camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setPreviewSize(3840, 2160)
xoutRgb = pipeline.create(dai.node.XLinkOut)

xoutRight.setStreamName("right")
xoutLeft.setStreamName("left")
xoutRgb.setStreamName("rgb")

# Properties
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Linking
monoRight.out.link(xoutRight.input)
monoLeft.out.link(xoutLeft.input)
camRgb.preview.link(xoutRgb.input)


# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queue will be used to get the grayscale frames from the output defined above
    qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)
    qLeft = device.getOutputQueue(name="left", maxSize=4, blocking=False)
    qRGB = device.getOutputQueue(name="rgb")

    dirName = "mono_data"
    Path(dirName).mkdir(parents=True, exist_ok=True)
    colordirName = "color_data"
    Path(colordirName).mkdir(parents=True, exist_ok=True)
    
    for i in range(50):
        inRight = qRight.get()
        inLeft = qLeft.get()
        inRgb = qRGB.get()

    i = 0
    while(i<5):
        time.sleep(1)

        inRight = qRight.get()  # Blocking call, will wait until a new data has arrived
        inLeft = qLeft.get()
        inRgb = qRGB.get()

        #cv2.imshow("Image", inRgb.getCvFrame())

        # After showing the frame, it's being stored inside a target directory as a PNG image
        t = str(int(time.time()))
        cv2.imwrite(f"{dirName}/Right_{t}.png", inRight.getFrame())
        cv2.imwrite(f"{dirName}/Left_{t}.png", inLeft.getFrame())
        cv2.imwrite(f"{colordirName}/Rgb_{t}.png", inRgb.getCvFrame())
        
        i += 1