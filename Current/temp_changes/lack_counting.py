#!/usr/bin/env python3

import cv2
import depthai as dai


pipeline = dai.Pipeline()

#mono camera
monoA= pipeline.create(dai.node.MonoCamera)
monoA.setFps(30)
#ImageManip node. Capability to crop, resize, warp, … incoming image frames
manipA = pipeline.create(dai.node.ImageManip)
#XLinkOut node. Sends messages over XLink.
manipOutA = pipeline.create(dai.node.XLinkOut)
#controlXlinkin
controlIn = pipeline.create(dai.node.XLinkIn)

controlIn.setStreamName('control')
manipOutA.setStreamName("right")


#specify which socket using
monoA.setBoardSocket(dai.CameraBoardSocket.CAM_A) 
monoA.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

manipA.setMaxOutputFrameSize(monoA.getResolutionHeight()*monoA.getResolutionWidth()*3)



#Input for CameraControl message, which can modify camera parameters in runtime
#Linking
controlIn.out.link(monoA.inputControl)
monoA.out.link(manipA.inputImage) 
manipA.out.link(manipOutA.input)



with dai.Device(pipeline) as device:
    qA = device.getOutputQueue(manipOutA.getStreamName(), maxSize=4, blocking=False)

    controlQueue = device.getInputQueue(controlIn.getStreamName())


    sensIso=200

    expTime_state1=1000
    expTime_state2=8000
    expTime=1000

    frame_lacking=0

    #ensure exposure_sent == exposure_received
    inA = qA.get()
    exposure_received=int(inA.getExposureTime().total_seconds()*1000000)
    exposure_sent=exposure_received


    while True:
        inA = qA.get()
        
        exposure_received=int(inA.getExposureTime().total_seconds()*1000000)

        #received exposure == sent exposure
        if(exposure_received == exposure_sent):   

            print(f"frame lacking = {frame_lacking}")
            #reset
            frame_lacking=0
        
        else:   #not receiving the sent exposure
            frame_lacking+=1
        

        #display image
        cv2.imshow("camA", inA.getCvFrame())
        key = cv2.waitKey(1)


        if(expTime==expTime_state1 and (exposure_received==exposure_sent)): #at stage 1 and received the sent exposure
            
            #send command to change to another state
            expTime=expTime_state2
            exposure_sent=expTime
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(expTime, sensIso)
            print("Setting manual exposure, time:", expTime, "iso:", sensIso)
            controlQueue.send(ctrl)

        
        elif(expTime==expTime_state2 and (exposure_received==exposure_sent)): #at stage 2 and received the sent exposure

            #send command to change to another state
            expTime=expTime_state1
            exposure_sent=expTime
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(expTime, sensIso)
            print("Setting manual exposure, time:", expTime, "iso:", sensIso)
            controlQueue.send(ctrl)


