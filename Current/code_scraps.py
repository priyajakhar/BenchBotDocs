image logging

first portion takes 124 ms, because cv2 imwrite takes time
second portion takes 14 ms
last portion takes 1.4



pipeline = dai.Pipeline()
pipeline.setXLinkChunkSize(0)

    device.setLogLevel(dai.LogLevel.DEBUG)
    device.setLogOutputLevel(dai.LogLevel.DEBUG)

    device.setLogLevel(dai.LogLevel.INFO)
    device.setLogOutputLevel(dai.LogLevel.INFO)


***************************************************************************
# changing buffer behaviour in camera

script.inputs['isp'].setBlocking(False)
script.inputs['isp'].setQueueSize(4)

# manip.inputImage.setBlocking(False)
# manip.inputImage.setQueueSize(2)

# videoEnc.input.setBlocking(False)
# videoEnc.input.setQueueSize(2)

xoutRgb.input.setBlocking(False)
xoutRgb.input.setQueueSize(2)

***************************************************************************

# warning messages in script node

script.setScript("""
    import time
    #node.warn(f"{Clock.now()}")
    while True:
        msg = node.io['cont'].tryGet()
        if msg is not None:
            #node.warn(f"{Clock.now()}")
            #node.warn(f"{time.time()}")
            t = Clock.now()
            diff = (t - msg.getTimestamp()).total_seconds() * 1000
            node.warn(f"{diff}")
""")

script.setProcessor(dai.ProcessorType.LEON_MSS)

***************************************************************************


# enabling jumbo frames

config = dai.Device.Config()
config.board.network.mtu = 9000 # Jumbo frames. Default 1500
config.board.network.xlinkTcpNoDelay = False # Default True
config.board.sysctl.append("net.inet.tcp.delayed_ack=1") # configure sysctl settings. 0 by default.

with dai.Device(config) as device:
    device.startPipeline(pipeline)



***************************************************************************

# save int data in txt file
        with open('latency.txt', 'w') as f:
            for it in diffs:
                f.write(str(it))
                f.write('\n')
        print(diffs)

        f = open('latency.txt', 'r')
        for x in f.readlines():
            print(x, end='')

***************************************************************************

    
    https://docs.luxonis.com/projects/api/en/latest/references/python/#depthai.MemoryInfo
    # print(device.getCmxMemoryUsage())
    # print(device.getDdrMemoryUsage())
    # print(device.getXLinkChunkSize())
    print(device.getCmxMemoryUsage().used)
    print(device.getDdrMemoryUsage().used)
    
    https://docs.luxonis.com/projects/api/en/latest/references/python/#depthai.CpuUsage
    print(device.getLeonCssCpuUsage(), device.getLeonCssCpuUsage().average)
    print(device.getLeonMssCpuUsage())
    
***************************************************************************
    
# to get an idea of ISO and SS adjustment of camera
    with open('ddata.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        while (time.time()-start < 50):
            imgFrame = feed.get()
            inRight = qRight.get()
            writer_object.writerow( [imgFrame.getSensitivity(), imgFrame.getExposureTime(), inRight.getSensitivity(), inRight.getExposureTime()] )
    f_object.close()
    # exp time is of type datetime.timedelta
    

                print("\n\nSeq no", self.nodes[frame_name].getSequenceNum(), "\n\n")
***************************************************************************


# putting images in a queue before saving them
    imgs = []
    for i in range(20):
        t = str(time.time())
        imgFrame = q.get()
        imgs.append(imgFrame)
        
    for im in imgs:
        t = str(time.time())
        im = cv2.imdecode(imgFrame.getData(), cv2.IMREAD_COLOR)
        cv2.imwrite(f"{dirName}/{t}_Rgb.jpg", im)
        
***************************************************************************
    # def test_get_seg(self):
        # seg_res = self.camera.get_seg()
        
        # with self.subTest():
            # assert((64, 64) == seg_res.shape), "Segmentation invalid size"
        # with self.subTest():
            # assert('float64' == seg_res.dtype), "Segmentation invalid data type"
            

segmentation_labels = segmentation_queue.get()
# original model
# seg_labels = (np.array(segmentation_labels.getFirstLayerFp16()).reshape(128,128)).astype(np.uint8)
# larger model
seg_labels = (np.array(segmentation_labels.getFirstLayerFp16()).reshape(64,64)).astype(np.uint8)
# smaller model
# seg_labels = (np.array(segmentation_labels.getFirstLayerInt32()).reshape(1024,1024)).astype(np.uint8)


***************************************************************************
# pipeline_graph run "python testing.py"


# import numpy as np
# from PIL import Image


# im2 = Image.open('dp.png')                                                                                             
# im2 = np.array(im2)

# print(im2.dtype, np.amax(im2))
# print(im2[10:15,10:15])


# inDisp = qDisp.tryGet()
# im = Image.fromarray(inDisp.getFrame())
# im.save(f"{dirname}/{t}_Disparity.png")




    # pipelines.append(['mono_enc_800', 'depth_sp_800'])
    # pipelines.append(['rgb_enc_1024', 'mono_800', 'depth_sp_800'])
    # pipelines.append(['rgb_1024', 'mono_800', 'depth_sp_800'])
    
    # pipelines.append(['rgb_enc_1024'])
    
    
    
    
                print(self.nodes[frame_name].getSequenceNum())
