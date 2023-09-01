#!/usr/bin/env python3

import time
import depthai as dai
import numpy as np
import cv2
import glob
import os, sys
import threading


class Camera():
    def __init__(self):
        
        self.pipeline = dai.Pipeline()
        self.pipeline.setOpenVINOVersion(version=dai.OpenVINO.VERSION_2021_4)

        self.RGB_Node = self.pipeline.createColorCamera()
        self.RGB_Node.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
        self.RGB_Node.setBoardSocket(dai.CameraBoardSocket.RGB)
        self.RGB_Node.setPreviewSize(1024,1024)
        self.RGB_Node.setVideoSize(2048, 2048)
        self.RGB_Node.setInterleaved(False)
  
        self.RGB_Out=self.pipeline.create(dai.node.XLinkOut)
        self.RGB_Out.setStreamName("rgb")
        self.RGB_Node.video.link(self.RGB_Out.input)

    def start_camera(self):
        self.device = dai.Device()
        self.device.startPipeline(self.pipeline)
        self.qRGB = self.device.getOutputQueue("rgb", 10, False)
        start = time.time()
        print("Started")
        while time.time()-start<10:
            rgb_in = self.qRGB.get()
            self.rgb_out = rgb_in.getCvFrame()
            time.sleep(0.1)
        print("Done")

    def get_rgb(self):
        return self.rgb_out

    def run(self):
        t1 = threading.Thread(target=self.start_camera)
        t1.start()
    
    def stop_camera(self):
        self.device.stop()
        # Closes the connection to device. Better alternative is the usage of context manager: with depthai.Device(pipeline) as device:

if __name__ == "__main__":
    camera1 = Camera()
    camera1.run()
    time.sleep(5)
    for i in range(5):
        print(i)
        t =  time.time()
        frame = camera1.get_rgb()
        cv2.imwrite(f"{t}_Rgb.jpg", frame)
        
    camera1.stop_camera()
