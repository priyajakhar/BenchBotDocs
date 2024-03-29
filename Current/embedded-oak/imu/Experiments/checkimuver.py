#!/usr/bin/env python3

import depthai as dai

# pipeline = dai.Pipeline()
# camRgb = pipeline.create(dai.node.ColorCamera)
# xoutRgb = pipeline.create(dai.node.XLinkOut)
# xoutRgb.setStreamName("rgb")
# camRgb.setPreviewSize(300, 300)
# camRgb.setInterleaved(False)
# camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
# camRgb.preview.link(xoutRgb.input)

camera_ip = "169.254.54.192"
cam = dai.DeviceInfo(camera_ip)

with dai.Device() as device:
    imuType = device.getConnectedIMU()
    imuFirmwareVersion = device.getIMUFirmwareVersion()
    print(f"IMU type: {imuType}, firmware version: {imuFirmwareVersion}")