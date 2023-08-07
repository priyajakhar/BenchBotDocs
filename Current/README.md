# Camera

### OAK_Camera.py
Contains class definition for oak camera where pipeline consists of RGB node, Left Right mono nodes and Depth node. The module can be imported in other python scripts and an instance of the OAK_Camera class can be created.

Function calls allow starting a camera, fetching specific frames and shutting down the camera.
![Diagram](class.jpg)

>> Example usage of the class is demonstrated in main.py.

#### Usage:

Initialize the Camera class object by passing the single parameter IP address of the camera you want to connect to.
```
camera = Camera("169.254.1.222")
```

Then use the below function to start the camera, which involves upload of firmware and pipeline with other assets (such as camera tuning blob, NN blob etc) 
```
camera.run()
```

As the upload of pipeline takes some time and input/output queues need to be initialized before we can start receiving frames (queues are located on the host computer in RAM), we need to wait for the camera to be ready or timeout to occur in case there are any errors when connecting to the camera.
```
timeout_start = time.time()
while not camera.camera_ready() and time.time() < ( timeout_start + 7 ):
	time.sleep(1)
```

In case of error, the program quits. 
```
if not camera.camera_ready():
	print("\nError: Couldn't connect to device!")
	sys.exit()
```

If connection to the camera is successfully established, then various frames can be fetched as described below. The frames have pre-defined names, if wrong frame name is used then returned value would be 'None'. 
>> Frame names: 'rgb', 'left', 'right', 'depth', 'disparity', 'segmentation'
```  
# fetch rgb frames
frame_rgb = camera.get_image('rgb')

# fetch right mono frame
frame_right = camera.get_image('right')

# fetch left mono frame
frame_left = camera.get_image('left')

# fetch depth frame
frame_depth = camera.get_image('depth')

# fetch disparity frame
frame_disparity = camera.get_image('disparity')

# fetch segmentation model output
frame_segmentation = camera.get_image('segmentation')
```

Once the program is done, the camera connection can be closed using
```
camera.stop_camera()
```

#### Other functions:

This function can be used to get the expected frame rate of the camera and the actual frame rate in order to verify if there's an issue that's preventing the camera from running at expected FPS.
```
expected_fps, actual_fps = camera.get_frame_rate()
```

This function can be used to get the exposure time (in ms) of incoming frames (currently it gives exposure time of RGB frame only). This can be used to verify if the upper limit of exposure time of frames is as expected.
```
exp_time = camera.get_exposure_time()
```

This function can be used to get the average CPU usage in terms of %. The utilization is of the 2 LeonCPUs available on the camera.
>> LeonOS (CSS Leon CPU) and LeonRT (MSS Leon CPU)
```
cpu_leonos, cpu_leonrt = camera.get_cpu_stats()
```



### test_OAK_Camera.py
Contains unit tests written for OAK_Camera


### camera_config.yaml
