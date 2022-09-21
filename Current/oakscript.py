## got the back up of this code
import cv2
import depthai as dai
import time

########################### OAK-D Funcs ###########################
def flushframes():
  for i in range(50):
    frame = queue.get()

def captureImage():
  flushframes()
  t = str(int(time.time()))
  filename = f"NC_OAK_{t}.PNG"
  frame = queue.get()
  imOut = frame.getCvFrame()
  cv2.imwrite(filename, imOut)

pipeline = dai.Pipeline()

# RGB
camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setPreviewSize(3840, 2160)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
xoutRgb = pipeline.create(dai.node.XLinkOut)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
xoutRgb.setStreamName("RGB")
camRgb.preview.link(xoutRgb.input)
device = dai.Device(pipeline)
queue = device.getOutputQueue(name="RGB")
flushframes()

###################################################################

# DEPTH
stereo = pipeline.create(dai.node.StereoDepth)
xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("DEPTH")

stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# LR-check is required for depth alignment
stereo.setLeftRightCheck(True)
stereo.setDepthAlign(dai.CameraBoardSocket.RGB)


# LEFT
left = pipeline.create(dai.node.MonoCamera)
left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
left.setBoardSocket(dai.CameraBoardSocket.LEFT)

# RIGHT
right = pipeline.create(dai.node.MonoCamera)
right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
right.setBoardSocket(dai.CameraBoardSocket.RIGHT)





queueNames.append("rgb")
queueNames.append("disp")

# Linking
camRgb.isp.link(rgbOut.input)
left.out.link(stereo.left)
right.out.link(stereo.right)
stereo.disparity.link(disparityOut.input)



# Capture Images
for i in range(1):
  print('Clicking picture....')
  time.sleep(2)
  captureImage()
  time.sleep(1)
