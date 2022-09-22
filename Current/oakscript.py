
Depth = pipeline.create(dai.node.StereoDepth)
xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("Disparity")

# Properties
# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
depth.setLeftRightCheck(True)
depth.setExtendedDisparity(False)
depth.setSubpixel(False)

# Linking
depth.disparity.link(xoutDepth.input)



qDepth = device.getOutputQueue(name="Disparity", maxSize=4, blocking=False)
inDisparity = qDepth.get()
frame = inDisparity.getFrame()
# Normalization for better visualization
frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
cv2.imshow("Disparity", frame)





# stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
# camRgb.isp.link(rgbOut.input)
