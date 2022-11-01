import cv2
import depthai as dai
import contextlib

# This can be customized to pass multiple parameters
def getPipeline():
    # Start defining a pipeline
    pipeline = dai.Pipeline()

    cam_rgb = pipeline.create(dai.node.ColorCamera)
    cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
    cam_rgb.setInterleaved(False)
    cam_rgb.initialControl.setSharpness(0)     # range: 0..4, default: 1		
    cam_rgb.initialControl.setLumaDenoise(0)   # range: 0..4, default: 1		
    cam_rgb.initialControl.setChromaDenoise(4) # range: 0..4, default: 1

    xout_rgb = pipeline.create(dai.node.XLinkOut)
    xout_rgb.setStreamName("rgb")
    cam_rgb.isp.link(xout_rgb.input)

    monoRight = pipeline.create(dai.node.MonoCamera)
    monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

    xoutRight = pipeline.create(dai.node.XLinkOut)
    xoutRight.setStreamName("right")
    monoRight.out.link(xoutRight.input)

    return pipeline


with contextlib.ExitStack() as stack:
    device_infos = dai.Device.getAllAvailableDevices()
    if len(device_infos) == 0:
        raise RuntimeError("No devices found!")
    devices = {}

    for device_info in device_infos:
        openvino_version = dai.OpenVINO.Version.VERSION_2021_4
        device = stack.enter_context(dai.Device(openvino_version, device_info, False))
        mxid = device.getMxId()

        # Get a customized pipeline based on identified device type
        pipeline = getPipeline()
        device.startPipeline(pipeline)

        # Output queue will be used to get the rgb frames from the output defined above
        devices[mxid] = {
            'rgb': device.getOutputQueue(name="rgb", maxSize=1, blocking=False),
            'right': device.getOutputQueue(name="right", maxSize=1, blocking=False),
        }

    n = 5
    i = 0
        
    while(i<n):
        for mxid, q in devices.items():
            if q['rgb'].has():
                color = q['rgb'].get().getCvFrame()
                monor = q['right'].get().getFrame()

                cv2.imwrite(f"{i}_Rgb.png", color)
                cv2.imwrite(f"{i}_Right.png", monor)
                i += 1

        if cv2.waitKey(1) == ord('q'):
            break