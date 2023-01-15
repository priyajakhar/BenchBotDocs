# crop isp feed to feed to videoencoder
#!/usr/bin/env python3
import time

from pathlib import Path
import cv2
import depthai as dai

# Create pipeline
pipeline = dai.Pipeline()

camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)

manip = pipeline.create(dai.node.ImageManip)
manip.initialConfig.setCropRect(0.006, 0, 1, 1)
#manip.initialConfig.setResize(4032, 3040)
manip.setNumFramesPool(2)
manip.setMaxOutputFrameSize(18385920)

camRgb.isp.link(manip.inputImage)

xoutRgb = pipeline.create(dai.node.XLinkOut)
xoutRgb.setStreamName("rgb")
manip.out.link(xoutRgb.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)

    # Make sure the destination path is present before starting to store the examples
    dirName = "rgb_data"
    Path(dirName).mkdir(parents=True, exist_ok=True)
    for r in range(30):
        c = qRgb.get()
    n = 2

    i = 0
    while(i<n):
        t = str(time.time())
        inRgb = qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise
        if inRgb is not None:
             cv2.imwrite(f"{dirName}/{t}_Rgb.png", inRgb.getCvFrame())
             i += 1