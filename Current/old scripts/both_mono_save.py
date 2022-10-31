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

xoutRight.setStreamName("right")
xoutLeft.setStreamName("left")


# Properties
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)


# Linking
monoRight.out.link(xoutRight.input)
monoLeft.out.link(xoutLeft.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queue will be used to get the grayscale frames from the output defined above
    qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)
    qLeft = device.getOutputQueue(name="left", maxSize=4, blocking=False)

    dirName = "mono_data"
    Path(dirName).mkdir(parents=True, exist_ok=True)
    i = 0

    while(i<5):
        inRight = qRight.get()  # Blocking call, will wait until a new data has arrived
        inLeft = qLeft.get()
        # Data is originally represented as a flat 1D array, it needs to be converted into HxW form
        # Frame is transformed and ready to be shown
        cv2.imshow("right", inRight.getCvFrame())
        cv2.imshow("left", inLeft.getCvFrame())

        # After showing the frame, it's being stored inside a target directory as a PNG image
        cv2.imwrite(f"{dirName}/Right{int(time.time() * 1000)}.png", inRight.getFrame())
        cv2.imwrite(f"{dirName}/Left{int(time.time() * 1000)}.png", inLeft.getFrame())

        time.sleep(4)
        i += 1