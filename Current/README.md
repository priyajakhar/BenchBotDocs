# Logging

System to log event data for debugging and to also capture and store outputs of the system for later analysis (biomass information / sample images / GPS records). This module will also evaluate the health of the rest of the systems running onboard the multi-camera setup. 

Logs will be stored in internal storage and will also be accessible from the API. 

There are 2 logging functions available:
> Camera Log
  > camera_connection_status(cam_id, connected)
  > arguments:
    > cam_id: camera ID for which status needs to be logged
    > connected: a boolean flag to determine connection status, True for connected and False for disconnected

> Image Log
  > log_image(cam, img_array, img_type, gps_tag, delete)
  > arguments:
    > cam: camera ID from which the image originates
    > img_array: image numpy array
    > img_type: image category such as 'RGB', 'Mono', 'Depth', etc
    > gps_tag: lattitude and longitude to be embedded into the image
    > delete: a boolean flag to determine if image needs to be deleted after it's archived