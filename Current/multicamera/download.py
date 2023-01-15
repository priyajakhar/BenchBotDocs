# simple program to download 12 MP RGB images, to be used for multicamera system
#!/usr/bin/env python3

import cv2
import depthai as dai
import sys, time

dirName = "oak_images"

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
camRgb.setInterleaved(False)

xoutRgb = pipeline.create(dai.node.XLinkOut)
xoutRgb.setStreamName("rgb")
camRgb.isp.link(xoutRgb.input)

cam = dai.DeviceInfo(sys.argv[1]) # IP

# Connect to device and start pipeline
with dai.Device(pipeline, cam) as device:
#with dai.Device(pipeline) as device:

	print('Connected')

	# Output queue will be used to get the rgb frames from the output defined above
	qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

	for r in range(50):
		inRgb = qRgb.get()
	i = 0
	n = 10
	cid = sys.argv[2]
	while i<n:
		t = str(time.time())
		inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived

		# Retrieve 'bgr' (opencv format) frame
		#cv2.imshow("rgb", inRgb.getCvFrame())
		cv2.imwrite(f"{dirName}/{t}_Rgb{cid}.png", inRgb.getCvFrame())
		i += 1
		time.sleep(0.1)

print("Done")
