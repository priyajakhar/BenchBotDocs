import depthai as dai
from pathlib import Path
import os

dirName = "oak_images"
Path(dirName).mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    
    device_infos = ["169.254.54.195", "169.254.54.200", "169.254.54.205"]
    # device_infos = ["169.254.54.200"]
    print("Found", len(device_infos), "devices")

    idx = 1
    for dev in device_infos:

        # commd = "python stream.py "+str(dev)+" &"
        commd = "python download.py "+str(dev)+" "+str(idx)+" &"
        # print(commd)
        os.system(commd)
        idx += 1

    print('Main Done')
