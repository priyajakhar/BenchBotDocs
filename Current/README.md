# Camera

-------
### OAK_Camera.py
Contains class definition for oak camera where pipeline consists of RGB node, Left Right mono nodes and Depth node. The module can be imported in other python scripts and an instance of the OAK_Camera class can be created.

Method calls allow starting a camera, fetching specific frames and shutting down the camera.

* Example usage is demonstrated in main.py.

### test_OAK_Camera.py
Contains unit tests written for OAK_Camera

-------
### OAK_Camera_Seg.py
Contains class definition for oak camera where the pipeline consists of RGB node, Depth node and NN nodel for segmentation model. The module usage is similar to OAK_Camera.

### test_OAK_Camera_seg.py
Contains unit tests written for OAK_Camera_Seg
-------