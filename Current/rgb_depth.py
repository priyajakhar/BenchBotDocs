import time
from pathlib import Path
import cv2
import depthai as dai
import numpy as np


dirName = "oak_images"

def dirsetup():
    Path(dirName).mkdir(parents=True, exist_ok=True)


# Create pipeline
pipeline = dai.Pipeline()

camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
camRgb.setInterleaved(False)
camRgb.initialControl.setSharpness(0)     # range: 0..4, default: 1		
camRgb.initialControl.setLumaDenoise(0)   # range: 0..4, default: 1		
camRgb.initialControl.setChromaDenoise(4) # range: 0..4, default: 1

xoutRgb = pipeline.create(dai.node.XLinkOut)
xoutRgb.setStreamName("rgb")
camRgb.video.link(xoutRgb.input)

xin = pipeline.create(dai.node.XLinkIn)
xin.setStreamName("control")
xin.out.link(camRgb.inputControl)

# Properties
videoEnc = pipeline.create(dai.node.VideoEncoder)
videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
camRgb.still.link(videoEnc.input)

# Linking
xoutStill = pipeline.create(dai.node.XLinkOut)
xoutStill.setStreamName("still")
videoEnc.bitstream.link(xoutStill.input)


# Depth camera
monoRight = pipeline.create(dai.node.MonoCamera)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)


monoLeft = pipeline.create(dai.node.MonoCamera)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)


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


# Connect to device and start pipeline
with dai.Device(pipeline) as device:
	
	dirsetup()
	
	qRGB = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
	qStill = device.getOutputQueue(name="still", maxSize=4, blocking=True)
	qDepth = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
	qControl = device.getInputQueue(name="control")

	while True:
		inRgb = qRGB.tryGet()

		if inRgb is not None:
			frame = inRgb.getCvFrame()
			frame = cv2.pyrDown(frame)
			frame = cv2.pyrDown(frame)
			cv2.imshow("Camera View", frame)

		if qStill.has():
			t = str(int(time.time()))
			
			fName = f"{dirName}/{t}_Rgb.png"
			with open(fName, "wb") as f:
				f.write(qStill.get().getData())
				print('Image saved')

			inDepth = qDepth.get()
			dframe = inDepth.getFrame()
			dframe = (dframe * (255 / Depth.initialConfig.getMaxDisparity())).astype(np.uint8)
			cv2.imwrite(f"{dirName}/{t}_Depth.png", dframe)
     
		key = cv2.waitKey(1)
		if key == ord('q'):
			break
		elif key == ord('c'):
			ctrl = dai.CameraControl()
			ctrl.setCaptureStill(True)
			qControl.send(ctrl)
			print("Sent 'still' event to the camera!")
