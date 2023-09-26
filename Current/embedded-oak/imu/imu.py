#!/usr/bin/env python3

import time
import depthai as dai
import cv2
import threading
import os
import numpy as np
import yaml
from from_root import from_root, from_here
import math

class Camera():
    def __init__(self, camera_ip):
        # dictionary for containing all the nodes in the pipeline
        self.nodes = dict()
        # flag to control closing of connection to the device (camera) 
        self.stop_flag = False
        # check whether camera is ready for fetching frames
        self.ready = False

        # create pipeline
        self.pipeline = dai.Pipeline()

        imu = self.pipeline.create(dai.node.IMU)
        # imu.enableFirmwareUpdate(True)

        # imu.enableIMUSensor([dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 100)
        # imu.enableIMUSensor(dai.IMUSensor.ACCELEROMETER_RAW, 500)
        # imu.enableIMUSensor(dai.IMUSensor.ACCELEROMETER, 50)
        imu.enableIMUSensor(dai.IMUSensor.GYROSCOPE_CALIBRATED, 25)
        imu.enableIMUSensor(dai.IMUSensor.ROTATION_VECTOR, 50)

        imu.setBatchReportThreshold(1)
        imu.setMaxBatchReports(10)
        
        xlinkOut = self.pipeline.create(dai.node.XLinkOut)
        xlinkOut.setStreamName("imu")
        imu.out.link(xlinkOut.input)
        self.nodes.update({'imu': None})
        
        
               
    def start_camera(self):
        def timeDeltaToMilliS(delta) -> float:
            return delta.total_seconds()*1000
            
        def timediff(val1, val2) -> float:
            res = (val1 - val2).total_seconds()
            return res
            
        GyroX, GyroY, GyroZ = 0, 0, 0
        gyroAngleX, gyroAngleY, gyroAngleZ = 0, 0, 0
        roll, pitch, yaw = 0, 0, 0
        GyroErrorX, GyroErrorY, GyroErrorZ = 0, 0, 0
        elapsedTime, currentTime, previousTime = [None], [None], [None]
        
        # array for device queues
        queues = []
        gx = []
        gy = []
        gz = []
        
        
        with dai.Device(self.pipeline) as device:
            device.startIMUFirmwareUpdate()
            
            imuType = device.getConnectedIMU()
            print(imuType)
            # if imuType != "BNO086":
                # print("Rotation vector output is supported only by BNO086!")
                # exit(1)
            
            # initializing the queue
            for idx, node_name in enumerate(self.nodes):
                queues.append( device.getOutputQueue(node_name, 50, False) )
            
            pcks = 0
            baseTs = None
            while True:
                # fetch frames from all queues
                for idx, node_name in enumerate(self.nodes):
                    self.nodes[node_name] = queues[idx].get()

                imuPackets = self.nodes[node_name].packets
                if pcks<5:
                    print(len(imuPackets))
                    pcks +=1
                    
                for imuPacket in imuPackets:
                    '''
                    '''
                    gyroValues = imuPacket.gyroscope
                    GyroX, GyroY, GyroZ = gyroValues.x, gyroValues.y, gyroValues.z
                    
                    currentTime[0] = gyroValues.getTimestampDevice()
                    if previousTime[0] is None:
                        previousTime = currentTime
                    elapsedTime[0] = timediff(currentTime[0], previousTime[0])
                    previousTime = currentTime
                    
                    # Correct the outputs with the calculated error values
                    GyroX += GyroErrorX
                    GyroY += GyroErrorY
                    GyroZ += GyroErrorZ
                    
                    # currentTime = time.time()
                    # elapsedTime = (currentTime - previousTime)
                    # previousTime = currentTime
                    
                    
                    
                    # Currently the raw values are in degrees per seconds, deg/s, so we need to multiply by sendonds (s) to get the angle in degrees
                    gyroAngleX += GyroX * elapsedTime[0]
                    gyroAngleY += GyroY * elapsedTime[0]
                    gyroAngleZ += GyroZ * elapsedTime[0]                    
                    # roll, pitch, yaw = gyroAngleX, gyroAngleY, gyroAngleZ
                    
                    # print(gyroAngleX, gyroAngleY, gyroAngleZ, "\n")

                    gx.append(GyroX)
                    gy.append(GyroY)
                    gz.append(GyroZ)
                    
                    # gx.append(gyroAngleX)
                    # gy.append(gyroAngleY)
                    # gz.append(gyroAngleZ)
                    
                    
                    rVvalues = imuPacket.rotationVector
                    imuF = "{:.06f}"
                    print(f"Quaternion: i: {imuF.format(rVvalues.i)} j: {imuF.format(rVvalues.j)} "
                        f"k: {imuF.format(rVvalues.k)} real: {imuF.format(rVvalues.real)}")
                    '''
                        demo code
                    '''
                    # acceleroValues = imuPacket.acceleroMeter
                    # gyroValues = imuPacket.gyroscope

                    # acceleroTs = acceleroValues.getTimestampDevice()
                    # gyroTs = gyroValues.getTimestampDevice()
                    # if baseTs is None:
                        # baseTs = acceleroTs if acceleroTs < gyroTs else gyroTs
                    # acceleroTs = timeDeltaToMilliS(acceleroTs - baseTs)
                    # gyroTs = timeDeltaToMilliS(gyroTs - baseTs)

                    # imuF = "{:.06f}"
                    # tsF  = "{:.03f}"

                    # print(f"Accelerometer timestamp: {tsF.format(acceleroTs)} ms")
                    # print(f"Accelerometer [m/s^2]: x: {imuF.format(acceleroValues.x)} y: {imuF.format(acceleroValues.y)} z: {imuF.format(acceleroValues.z)}")
                    # print(f"Gyroscope timestamp: {tsF.format(gyroTs)} ms")
                    # print(f"Gyroscope [rad/s]: x: {imuF.format(gyroValues.x)} y: {imuF.format(gyroValues.y)} z: {imuF.format(gyroValues.z)}\n ")

                if cv2.waitKey(1) == ord('q'):
                    break
                    
                if self.stop_flag:
                    break
                time.sleep(0.1)
                
                if not self.ready:
                    self.ready = True

        with open('gyrox.txt', 'w') as f:
            for d in gx:
                f.write(str(d))
                f.write('\n')
        with open('gyroy.txt', 'w') as f:
            for d in gy:
                f.write(str(d))
                f.write('\n')
        with open('gyroz.txt', 'w') as f:
            for d in gz:
                f.write(str(d))
                f.write('\n')
            
    def run(self):
        t1 = threading.Thread(target=self.start_camera)
        t1.start()
    
    def camera_ready(self):
        return self.ready

    def stop_camera(self):
        # flag to signal termination of connection to camera
        self.stop_flag = True


# def get_imu_error():
    # n = 100
    # for i in range(n):
        # GyroX, GyroY, GyroZ = imuPacket.gyroscope
        # GyroErrorX += (GyroX / 131.0)
        # GyroErrorY += (GyroY / 131.0)
        # GyroErrorZ += (GyroZ / 131.0)
    # GyroErrorX /= n
    # GyroErrorY /= n
    # GyroErrorZ /= n