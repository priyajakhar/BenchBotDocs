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
  filename = f"NC_OAK_{t}.jpg"
  frame = queue.get()
  imOut = frame.getCvFrame()
  cv2.imwrite(filename, imOut)

pipeline = dai.Pipeline()
camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setPreviewSize(3840, 2160)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
xoutRgb = pipeline.create(dai.node.XLinkOut)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
xoutRgb.setStreamName("rgb")
camRgb.preview.link(xoutRgb.input)
device = dai.Device(pipeline)
queue = device.getOutputQueue(name="rgb")
flushframes()

###################################################################


# Capture Images
for i in range(1):
  print('Clicking picture....')
  time.sleep(2)
  captureImage()
  time.sleep(1)
