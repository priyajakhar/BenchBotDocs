import depthai as dai
from pathlib import Path
import os


dirName = "oak_images"
Path(dirName).mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    
    device_infos = dai.Device.getAllAvailableDevices()
    print("Found", len(device_infos), "devices")

    idx = 1
    for dev in device_infos:
        cam = dev.getMxId()
        commd = "python test2.py "+str(cam)+" "+str(idx)+" &"
        # print(commd)
        os.system(commd)
        idx += 1

    print('Devices closed')