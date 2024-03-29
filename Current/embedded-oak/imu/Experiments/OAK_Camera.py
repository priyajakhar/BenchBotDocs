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
import calib

'''
function to add a Script node to a pipeline
arguments: parent pipeline, input to the node, waittime variable for wait period between outputs
'''
def add_scriptnode(pipeline, inputlink, waittime):
    scriptnode = pipeline.createScript()
    inputlink.link(scriptnode.inputs['in_stream'])
    scriptnode.inputs['in_stream'].setBlocking(False)
    scriptnode.setScript(f"""
        import time
        mark = time.time()
        while True:
            if (time.time() - mark) > {waittime}:
                mark = time.time()
                frame = node.io['in_stream'].get()
                node.io['out'].send(frame)
            time.sleep(0.1)
    """)
    return scriptnode


'''
function to add a VideoEncoder node to a pipeline
arguments: parent pipeline, input to the node
'''
def add_videoencoder(pipeline, inputlink):
    videoEncoder = pipeline.create(dai.node.VideoEncoder)
    videoEncoder.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
    inputlink.link(videoEncoder.input)
    return videoEncoder
  
    
'''
    Camera() class defined for configuring and uploading specific pipeline to the oak camera
'''
class Camera():

    def __init__(self, camera_ip, file_path="camera/camera_config.yaml"):
        # loading the data from the camera configuration file
        config_file = from_root(file_path)
        with open(config_file, "r") as yamlfile:
            config_data = yaml.load(yamlfile, Loader=yaml.FullLoader)

        # FPS for all camera streams
        fps = config_data['fps']
        fps_3a = config_data['fps_3a']
        self.debug = config_data['debug']
        pipeline_type = config_data['pipeline']
        pipeline = config_data[pipeline_type]
        
        # IP address of the camera, to be used during pipeline upload
        self.camera_ip = camera_ip
        # dictionary for containing all the nodes in the pipeline
        self.nodes = dict()
        # dictionary for containing expected latency of frames from nodes
        self.frame_latency = dict()
        # flag to control closing of connection to the device (camera) 
        self.stop_flag = False
        # check whether camera is ready for fetching frames
        self.ready = False

        # create pipeline
        self.pipeline = dai.Pipeline()
        # specify OpenVINO version
        self.pipeline.setOpenVINOVersion(version=dai.OpenVINO.VERSION_2021_4)
        # define the path for camera tuning blob
        camera_tuning_blob_path = from_here(config_data['camera_tuning_blob'])
        self.pipeline.setCameraTuningBlobPath(camera_tuning_blob_path)

        ''' ColorCamera (RGB) node '''
        if 'RGB' in pipeline:
            preview_dims = tuple( pipeline['RGB']['preview'] )
            video_dims = tuple( pipeline['RGB']['video'] )
            rgb_xout = pipeline['RGB']['xout']
            self.rgb_encode = rgb_xout['encode']

            camRgb = self.pipeline.createColorCamera()
            camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
            camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
            camRgb.setPreviewSize(preview_dims)
            camRgb.setVideoSize(video_dims)
            camRgb.setInterleaved(False)
            if fps is not None:
                camRgb.setFps(fps)
            camRgb.setIsp3aFps(fps_3a)
            
            if rgb_xout['input'] is not None:
                xoutRgb = self.pipeline.create(dai.node.XLinkOut)
                xoutRgb.setStreamName("rgb")
                self.nodes.update({'rgb': None})
                self.frame_latency.update({'rgb': 1/fps})
                
                if rgb_xout['input'] == 'video':
                    in_link = camRgb.video
                else:
                    in_link = camRgb.preview
                
                time_gap = rgb_xout['time_gap']
                if time_gap > 0:
                    self.frame_latency['rgb'] = time_gap
                    script = add_scriptnode(self.pipeline, in_link, time_gap)
                    in_link = script.outputs['out']
                if self.rgb_encode:
                    videoEnc = add_videoencoder(self.pipeline, in_link)
                    in_link = videoEnc.bitstream              
                
                in_link.link(xoutRgb.input)

        ''' NeuralNetwork (Segmentaion model) node'''
        if 'Segmentation' in pipeline:
            self.seg_output_dims = tuple([pipeline['Segmentation']['output_dims']['w'], pipeline['Segmentation']['output_dims']['h']])
            nn_blob_path = from_root(pipeline['Segmentation']['blob_path'])
            nn_node = self.pipeline.create(dai.node.NeuralNetwork)
            nn_node.setBlobPath(nn_blob_path)
            nn_node.input.setBlocking(False)
            nn_node.input.setQueueSize(1)
            camRgb.preview.link(nn_node.input)

            seg_out = self.pipeline.create(dai.node.XLinkOut)
            seg_out.setStreamName("segmentation")
            nn_node.out.link(seg_out.input)
            self.nodes.update({'segmentation': None})
        
        ''' Right Left MonoCamera node '''     
        if 'Mono' in pipeline or 'Depth' in pipeline:
            mono_xout = pipeline['Mono']['xout']
            self.mono_encode = pipeline['Mono']['encode']

            monoRight = self.pipeline.create(dai.node.MonoCamera)
            monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
            monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

            monoLeft = self.pipeline.create(dai.node.MonoCamera)
            monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
            monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

            if fps is not None:
                monoRight.setFps(fps)
                monoLeft.setFps(fps)
            monoRight.setIsp3aFps(fps_3a)
            monoLeft.setIsp3aFps(fps_3a)
   
            # check and add if outputs of mono cameras are linked to host
            if mono_xout:
                xoutRight = self.pipeline.create(dai.node.XLinkOut)
                xoutRight.setStreamName("right")
                self.nodes.update({'right': None})
                self.frame_latency.update({'right': 1/fps})
                xoutLeft = self.pipeline.create(dai.node.XLinkOut)
                xoutLeft.setStreamName("left")
                self.nodes.update({'left': None})
                self.frame_latency.update({'left': 1/fps})
                
                r_in_link = monoRight.out
                l_in_link = monoLeft.out
                
                time_gap = pipeline['Mono']['time_gap']
                if time_gap > 0:
                    self.frame_latency['right'] = time_gap
                    self.frame_latency['left'] = time_gap
                    scriptRight = add_scriptnode(self.pipeline, r_in_link, time_gap)
                    r_in_link = scriptRight.outputs['out']
                    scriptLeft = add_scriptnode(self.pipeline, l_in_link, time_gap)
                    l_in_link = scriptLeft.outputs['out']
                if self.mono_encode:
                    videoEncRight = add_videoencoder(self.pipeline, r_in_link)
                    r_in_link = videoEncRight.bitstream
                    videoEncLeft = add_videoencoder(self.pipeline, l_in_link)
                    l_in_link = videoEncLeft.bitstream

                r_in_link.link(xoutRight.input)
                l_in_link.link(xoutLeft.input)
        
        ''' StereoDepth node '''
        if 'Depth' in pipeline:
            subpixel = pipeline['Depth']['subpixel']
            disparity = pipeline['Depth']['disparity']

            Depth = self.pipeline.create(dai.node.StereoDepth)
            Depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
            Depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
            Depth.setLeftRightCheck(True)
            Depth.setExtendedDisparity(False)
            if subpixel:   Depth.setSubpixel(True)
            else:   Depth.setSubpixel(False)

            xoutDepth = self.pipeline.create(dai.node.XLinkOut)
            monoRight.out.link(Depth.right)
            monoLeft.out.link(Depth.left)
            if disparity:
                Depth.disparity.link(xoutDepth.input)
                xoutDepth.setStreamName("disparity")
                self.nodes.update({'disparity': None})
            else:
                Depth.depth.link(xoutDepth.input)
                xoutDepth.setStreamName("depth")
                self.nodes.update({'depth': None})
            self.frame_latency.update({'depth': 1/fps})

        ''' IMU node '''
        if 'IMU' in pipeline:
            imu_node = pipeline['IMU']
            self.Soffset = imu_node['Soft-bias']
            self.Hoffset = imu_node['Hard-bias']
            self.Declination = imu_node['Declination']
            mfreq = imu_node['Mag']['freq']
            afreq = imu_node['Acc']['freq']
            imu = self.pipeline.create(dai.node.IMU)
            imu.enableIMUSensor(dai.IMUSensor.ACCELEROMETER, afreq)
            imu.enableIMUSensor(dai.IMUSensor.MAGNETOMETER_CALIBRATED, mfreq)
            # imu.enableIMUSensor(dai.IMUSensor.MAGNETOMETER_RAW, mfreq)
            imu.setBatchReportThreshold(1)
            imu.setMaxBatchReports(10)
            
            xoutImu = self.pipeline.create(dai.node.XLinkOut)
            xoutImu.setStreamName("imu")
            imu.out.link(xoutImu.input)
            self.nodes.update({'imu': None})

            # print(apply_iron_offsets([34.3, 45.2, 34.2], self.Soffset, self.Hoffset))

    def start_camera(self):
        # array for device queues
        queues = []
        # dictionary to store time differences between frame fetches per queue
        self.time_diffs = dict()
        # array to store previous frame times per queue
        prev_time = []
        
        cam = dai.DeviceInfo(self.camera_ip)
        config = dai.Device.Config()
        # config.board.network.mtu = 9000
        config.board.network.xlinkTcpNoDelay = False
        # config.board.sysctl.append("net.inet.tcp.delayed_ack=1")
        
        # upload the pipeline to the device
        try:
            with dai.Device(config) as device:
                device.startPipeline(self.pipeline)
                device.startIMUFirmwareUpdate()
                
                # check for debugging enabled for device
                if self.debug:
                    device.setLogLevel(dai.LogLevel.INFO)
                    device.setLogOutputLevel(dai.LogLevel.INFO)

                # initializing the queue
                for idx, node_name in enumerate(self.nodes):
                    queues.append( device.getOutputQueue(node_name, 2, False) )
                    self.time_diffs.update({node_name: []})
                    prev_time.append(time.time())

                while True:
                    # fetch frames from all queues
                    for idx, node_name in enumerate(self.nodes):
                        new_frame = queues[idx].tryGet()
                        if new_frame is not None:
                            self.nodes[node_name] = new_frame
                            self.time_diffs[node_name].append(time.time()-prev_time[idx])
                            prev_time[idx] = time.time()

                    # CPU consumption stats
                    self.leonos = device.getLeonCssCpuUsage().average
                    self.leonrt = device.getLeonMssCpuUsage().average

                    if self.stop_flag:
                        break

                    if not self.ready:
                        self.ready = True
                        
                    time.sleep(0.05)
        except RuntimeError as err:
            print(err)
           
    def run(self):
        t1 = threading.Thread(target=self.start_camera)
        t1.start()
    
    def camera_ready(self):
        return self.ready

    def stop_camera(self):
        # flag to signal termination of connection to camera
        self.stop_flag = True

    def get_image(self, frame_name):
        try:
            if frame_name == 'rgb':
                if self.rgb_encode:
                    rgb_out = self.nodes[frame_name].getData()
                    rgb_frame = cv2.imdecode(rgb_out, cv2.IMREAD_COLOR)
                else:
                    rgb_frame = self.nodes[frame_name].getCvFrame()
                return rgb_frame
            elif frame_name == 'segmentation':
                seg_out = self.nodes[frame_name].getFirstLayerFp16()
                seg_frame = np.array(seg_out).reshape(self.seg_output_dims).astype(np.uint8)
                return seg_frame
            elif frame_name in ('left', 'right'):
                if self.mono_encode:
                    mono_out = self.nodes[frame_name].getData()
                    mono_frame = cv2.imdecode(mono_out, 0)
                else:
                    mono_frame = self.nodes[frame_name].getFrame()
                return mono_frame
            else:
                f_out = self.nodes[frame_name].getFrame()
                return f_out
        except:
            return None
    
    def get_frame_rate(self, nodename=None):
        # return the expected and actual latency of frames in camera streams
        if nodename is None:
            nodename = list(self.time_diffs)[-1]
        try:
            arr = self.time_diffs[nodename]
            if len(arr) > 0:
                res = np.average( np.array(arr) )
            else:
                res = 0
            return self.frame_latency[nodename], res
        except:
            return None, None

    def get_exposure_time(self):
        # return the exposure time of rgb frame
        exp_time = self.nodes['rgb'].getExposureTime()
        return exp_time
        
    def get_cpu_stats(self):
        # return LeonOS and LeonRT consumption stats in %
        return [round(self.leonos*100), round(self.leonrt*100)]
    
    def get_imu_reading(self):    
        # try:
        imuPackets = self.nodes['imu'].packets
        for imuPacket in imuPackets:
            mFvalues = imuPacket.magneticField
            aValues = imuPacket.acceleroMeter
            imu_data = self.process_data(mFvalues, aValues)
            # print(imu_data)
            return imu_data                
        # except:
        #     self.stop_camera()
    
    def process_data(self, mag, acc):
        # mx, my, mz = mag[0], mag[1], mag[2]
        mx, my, mz = mag.x, mag.y, mag.z
        # data_arr = [acc.x, acc.y, acc.z]

        '''New calibration process'''
        caliba = False
        if caliba==True:
            data_arr = [mx,my,mz]
            print(data_arr)
        else:
            mx, my = calib.transform_data(mx,my,mz)
            heading = calc_heading(my, mx, self.Declination)
            print(heading)
            data_arr = [my, mx, round(heading, 2)]

        '''After calibration is done'''
        # ax, ay, az = acc.x, acc.y, acc.z
        # mx, my = tilt_comp(mx, my, mz, ax, ay, az)
        # mx, my, mz = apply_iron_offsets([mx, my, mz], self.Soffset, self.Hoffset)

        return data_arr
    
def apply_iron_offsets(magneto, s_offset, h_offset):
    # apply hard-iron offset
    hard_iron, soft_iron = [], []
    for i in range(3):
        hard_iron.append(magneto[i]-h_offset[i])
    # print(hard_iron)
    # apply soft-iron offset
    for i in range(3):
        res = 0
        for j in range(3):
            res += s_offset[i][j] * hard_iron[j]
        soft_iron.append(res)
    # print(soft_iron)
    return soft_iron

def tilt_comp(mx, my, mz, ax, ay, az):
    # Calculate pitch and roll
    pitch = math.atan2(ax, math.sqrt(ay**2 + az**2))
    roll = math.atan2(ay, math.sqrt(ax**2 + az**2))
    # Tilt compensate magnetometer readings
    mag_x = mx * math.cos(pitch) + mz * math.sin(pitch)
    mag_y = mx * math.sin(roll) * math.sin(pitch) + my * math.cos(roll) - mz * math.sin(roll) * math.cos(pitch)

    # mag_y = my * math.cos(pitch) + mz * math.sin(pitch)
    # mag_x = my * math.sin(roll) * math.sin(pitch) + mx * math.cos(roll) - mz * math.sin(roll) * math.cos(pitch)
    return mag_x, mag_y

def calc_heading(y, x, declination):
    # Calculate heading
    heading = math.atan2(-y, x)
    # Convert heading from radians to degrees
    heading_deg = math.degrees(heading)
    # compensate for declination angle
    heading_deg += declination
    # Adjust heading to be between 0 and 360 degrees
    heading_deg +=180
    # if heading_deg<0: heading_deg += 360
    return heading_deg