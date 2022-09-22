# DEPTH
stereo = pipeline.create(dai.node.StereoDepth)
xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("DEPTH")

stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# LR-check is required for depth alignment
stereo.setLeftRightCheck(True)
stereo.setDepthAlign(dai.CameraBoardSocket.RGB)


queueNames.append("rgb")
queueNames.append("disp")

# Linking
camRgb.isp.link(rgbOut.input)
left.out.link(stereo.left)
right.out.link(stereo.right)
stereo.disparity.link(disparityOut.input)
