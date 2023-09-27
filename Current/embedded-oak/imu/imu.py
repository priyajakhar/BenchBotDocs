#!/usr/bin/env python3

import time
import depthai as dai
import cv2
import threading
import os, sys
import numpy as np
import yaml
from from_root import from_root, from_here
import math

 
def to_degrees(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    # Convert from radians to degrees
    roll, pitch, yaw = [math.degrees(roll_x), math.degrees(pitch_y), math.degrees(yaw_z)]
    # return roll_x, pitch_y, yaw_z
    return roll, pitch, yaw

'''
    demo code
'''
def timeDeltaToMilliS(delta) -> float:
    return delta.total_seconds()*1000

def demo_code(packet, baseTs):
    acceleroValues = packet.acceleroMeter
    gyroValues = packet.gyroscope

    acceleroTs = acceleroValues.getTimestampDevice()
    gyroTs = gyroValues.getTimestampDevice()
    if baseTs is None:
        baseTs = acceleroTs if acceleroTs < gyroTs else gyroTs
    acceleroTs = timeDeltaToMilliS(acceleroTs - baseTs)
    gyroTs = timeDeltaToMilliS(gyroTs - baseTs)

    imuF = "{:.06f}"
    tsF  = "{:.03f}"

    print(f"Accelerometer timestamp: {tsF.format(acceleroTs)} ms")
    print(f"Accelerometer [m/s^2]: x: {imuF.format(acceleroValues.x)} y: {imuF.format(acceleroValues.y)} z: {imuF.format(acceleroValues.z)}")
    print(f"Gyroscope timestamp: {tsF.format(gyroTs)} ms")
    print(f"Gyroscope [rad/s]: x: {imuF.format(gyroValues.x)} y: {imuF.format(gyroValues.y)} z: {imuF.format(gyroValues.z)}\n ")
    
    return baseTs

'''
    my code for gyroscope
'''
def timediff(val1, val2) -> float:
    res = (val1 - val2).total_seconds()
    return res

rtype = None
GyroErrorX, GyroErrorY, GyroErrorZ = 0, 0, 0
           
def my_code(packet, previousTime, angles):
    gyroValues = packet.gyroscope
    GyroX, GyroY, GyroZ = gyroValues.x, gyroValues.y, gyroValues.z
    # Correct the outputs with the calculated error values
    # GyroX += GyroErrorX
    # GyroY += GyroErrorY
    # GyroZ += GyroErrorZ
    
    currentTime = gyroValues.getTimestampDevice()
    if previousTime is None:
        previousTime = currentTime
    elapsedTime = timediff(currentTime, previousTime)
    previousTime = currentTime
    
    # Currently the raw values are in degrees per seconds, deg/s, so we need to multiply by sendonds (s) to get the angle in degrees
    # roll, pitch, yaw = gyroAngleX, gyroAngleY, gyroAngleZ
    gyroAngleX, gyroAngleY, gyroAngleZ = angles
    gyroAngleX += GyroX * elapsedTime
    gyroAngleY += GyroY * elapsedTime
    gyroAngleZ += GyroZ * elapsedTime
    angles = [gyroAngleX, gyroAngleY, gyroAngleZ]
    # print(gyroAngleX, gyroAngleY, gyroAngleZ, "\n")

    if rtype == 'raw':
        readings = [GyroX, GyroY, GyroZ]
    elif rtype=='angle':
        readings = [gyroAngleX, gyroAngleY, gyroAngleZ]
    else:
        readings = None
    
    return previousTime, readings, angles
    

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
        # imu.enableIMUSensor(dai.IMUSensor.GYROSCOPE_CALIBRATED, 25)
        
        imu.enableIMUSensor(dai.IMUSensor.ROTATION_VECTOR, 50)

        imu.setBatchReportThreshold(1)
        imu.setMaxBatchReports(10)
        
        xlinkOut = self.pipeline.create(dai.node.XLinkOut)
        xlinkOut.setStreamName("imu")
        imu.out.link(xlinkOut.input)
        self.nodes.update({'imu': None})
               
    def start_camera(self):
            
        # GyroX, GyroY, GyroZ = 0, 0, 0
        # gyroAngleX, gyroAngleY, gyroAngleZ = 0, 0, 0
        gyroangles = [0, 0, 0]
        # roll, pitch, yaw = 0, 0, 0
        
        # elapsedTime, currentTime, previousTime = [None], [None], [None]
        previousTime = [None]
        
        # array for device queues
        queues = []
        gx, gy, gz = [], [], []
        
        
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
                    # for my code
                    # previousTime[0], data, gyroangles = my_code(imuPacket, previousTime[0], gyroangles)
                    # if data is not None:
                        # gx.append(data[0])
                        # gy.append(data[0])
                        # gz.append(data[0])
                    
                    # for rotation vector
                    rVvalues = imuPacket.rotationVector
                    if False:
                        imuF = "{:.06f}"
                        print(f"Quaternion: i: {imuF.format(rVvalues.i)} j: {imuF.format(rVvalues.j)} "
                            f"k: {imuF.format(rVvalues.k)} real: {imuF.format(rVvalues.real)}")
                    r, p, y = to_degrees(rVvalues.i, rVvalues.j, rVvalues.k, rVvalues.real)
                    print(r, p, y)
                    
                    # for demo code
                    # baseTs = demo_code(imuPacket, baseTs)

                   
                if self.stop_flag:
                    break
                time.sleep(0.1)
                
                if not self.ready:
                    self.ready = True
        
        record = False
        if record:
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




if __name__ == "__main__":
    camera = Camera("169.254.222.1")
    camera.run()
    timeout_start = time.time()
    timeout = 10
    while not camera.camera_ready() and time.time() < ( timeout_start + timeout ):
        time.sleep(1)
    if not camera.camera_ready():
        print("\nError: Couldn't connect to device!")
        sys.exit()
    time.sleep(2)
    camera.stop_camera()
    
    
    
    
    
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