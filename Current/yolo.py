# from hello world example, changed for yolov4_coco_608x608
from pathlib import Path

import blobconverter
import cv2
import depthai
import numpy as np

pipeline = depthai.Pipeline()

cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(608, 608)
cam_rgb.setInterleaved(False)

detection_nn = pipeline.createMobileNetDetectionNetwork()
detection_nn.setBlobPath(str(Path("models/yolov4_coco_608x608/yolov4_coco_608x608.blob").resolve().absolute()))
detection_nn.setConfidenceThreshold(0.5)
cam_rgb.preview.link(detection_nn.input)

xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

xout_nn = pipeline.createXLinkOut()
xout_nn.setStreamName("nn")
detection_nn.out.link(xout_nn.input)

with depthai.Device(pipeline) as device:
    device.setLogLevel(depthai.LogLevel.INFO)
    device.setLogOutputLevel(depthai.LogLevel.INFO)
    
    q_rgb = device.getOutputQueue("rgb")
    q_nn = device.getOutputQueue("nn")

    frame = None
    detections = []

    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    while True:
        in_rgb = q_rgb.tryGet()
        in_nn = q_nn.tryGet()

        if in_rgb is not None:
            frame = in_rgb.getCvFrame()

        if in_nn is not None:
            detections = in_nn.detections

        if frame is not None:
            for detection in detections:
                bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
            cv2.imshow("preview", frame)

        if cv2.waitKey(1) == ord('q'):
            break

# [14442C10913B11D100] [1.1] [9.224] [XLinkOut(3)] [error] Message has too much metadata (130799B) to serialize. Maximum is 51200B. Dropping message
# [14442C10913B11D100] [1.1] [11.855] [XLinkOut(3)] [error] Message has too much metadata (129231B) to serialize. Maximum is 51200B. Dropping message
# [14442C10913B11D100] [1.1] [11.918] [XLinkOut(3)] [error] Message has too much metadata (127295B) to serialize. Maximum is 51200B. Dropping message




# [14442C10913B11D100] [1.1] [7.749] [system] [info] Temperatures - Average: 32.91 ┬░C, CSS: 33.69 ┬░C, MSS 32.25 ┬░C, UPA: 33.21 ┬░C, DSS: 32.49 ┬░C
# [14442C10913B11D100] [1.1] [7.749] [system] [info] Cpu Usage - LeonOS 9.58%, LeonRT: 8.91%
# [14442C10913B11D100] [1.1] [7.912] [XLinkOut(3)] [error] Message has too much metadata (128555B) to serialize. Maximum is 51200B. Dropping message
# [14442C10913B11D100] [1.1] [8.750] [system] [info] Memory Usage - DDR: 308.64 / 340.61 MiB, CMX: 2.38 / 2.50 MiB, LeonOS Heap: 21.97 / 77.48 MiB, LeonRT Heap: 11.92 / 41.35 MiB
# [14442C10913B11D100] [1.1] [8.751] [system] [info] Temperatures - Average: 34.04 ┬░C, CSS: 35.11 ┬░C, MSS 34.16 ┬░C, UPA: 34.16 ┬░C, DSS: 32.73 ┬░C
# [14442C10913B11D100] [1.1] [8.751] [system] [info] Cpu Usage - LeonOS 20.36%, LeonRT: 35.32%
# [14442C10913B11D100] [1.1] [9.752] [system] [info] Memory Usage - DDR: 308.64 / 340.61 MiB, CMX: 2.38 / 2.50 MiB, LeonOS Heap: 21.97 / 77.48 MiB, LeonRT Heap: 11.92 / 41.35 MiB
# [14442C10913B11D100] [1.1] [9.752] [system] [info] Temperatures - Average: 33.57 ┬░C, CSS: 34.40 ┬░C, MSS 32.97 ┬░C, UPA: 33.69 ┬░C, DSS: 33.21 ┬░C
# [14442C10913B11D100] [1.1] [9.752] [system] [info] Cpu Usage - LeonOS 9.54%, LeonRT: 5.10%
# [14442C10913B11D100] [1.1] [10.073] [XLinkOut(3)] [error] Message has too much metadata (128023B) to serialize. Maximum is 51200B. Dropping message
# [14442C10913B11D100] [1.1] [10.134] [XLinkOut(3)] [error] Message has too much metadata (130179B) to serialize. Maximum is 51200B. Dropping message
# [14442C10913B11D100] [1.1] [10.754] [system] [info] Memory Usage - DDR: 308.64 / 340.61 MiB, CMX: 2.38 / 2.50 MiB, LeonOS Heap: 21.97 / 77.48 MiB, LeonRT Heap: 11.92 / 41.35 MiB

