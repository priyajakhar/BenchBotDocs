'''
Project logger
'''

from datetime import date
import time
import cv2
from pathlib import Path
from from_root import from_root, from_here
import csv
import os

main_path = from_root('')
sys.path.append(str(main_path))

from datetime import datetime

import json


Path("images_log").mkdir(parents=True, exist_ok=True)

fields = ['Timestamp', 'Connected', 'NotConnected']

# if csv file doesn't exist, create one
cam_status_file = Path('camera_status.csv')
if not cam_status_file.exists():
    with open(cam_status_file, 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writeheader()
    
num_of_cameras = 3
updates = 0

def log_image(img, img_type, gps_tag):
    date_obj = datetime.utcnow()
    day = date_obj.date()
    hour = date_obj.time().hour
    minutes = date_obj.time().minute

    fileName = f"{day}_{hour}:{minutes}_{img_type}.png"
    cv2.imwrite(fileName, img)


# writing current camera status to the csv file
def update_camera_status():
    camera_dict = [{'Timestamp': None, 'Connected': [], 'NotConnected': []} ]
    
    json_files = [cam_json for cam_json in os.listdir("images_log/") if cam_json.endswith('.json')]
    # print(json_files)
    
    for cam_file in json_files:
        with open("images_log/" + cam_file) as json_file:
            data = json.load(json_file)
            if data['Status'] == 'Connected':
                camera_dict[0]['Connected'].append(data['Camera_ID'])
            else:
                camera_dict[0]['NotConnected'].append(data['Camera_ID'])
    camera_dict[0]['Timestamp'] = datetime.utcnow()

    with open('camera_status.csv', 'a', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writerows(camera_dict)

def camera_status_log(cam_id, status):
    camera_dict = {'Camera_ID': cam_id, 'Timestamp': str(datetime.utcnow()), 'Status': status}
    fileName = f"images_log/Camera_{cam_id}.json"
    # print(fileName)
    with open(fileName, 'w') as fp:
        json.dump(camera_dict, fp)
    

camera_status_log(1, 'Connected')
camera_status_log(2, 'Connected')
camera_status_log(3, 'Connected')
camera_status_log(4, 'Connected')
camera_status_log(5, 'Connected')
update_camera_status()

# from exif import Image
# import piexif


# exif_dict = piexif.load("Rgb.jpg")
# print(exif_dict)


# with open('cat.png', 'rb') as image_file:
    # my_image = Image(image_file)

# print(my_image.has_exif)


# gps_ifd = {
        # piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        # piexif.GPSIFD.GPSAltitudeRef: 1,
        # piexif.GPSIFD.GPSAltitude: change_to_rational(round(altitude)),
        # piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        # piexif.GPSIFD.GPSLatitude: exiv_lat,
        # piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
        # piexif.GPSIFD.GPSLongitude: exiv_lng,
        # piexif.GPSIFD.GPSDateStamp: gpsTime
    
    # }

    # exif_dict = {"GPS": gps_ifd}
    # exif_bytes = piexif.dump(exif_dict)
    # piexif.insert(exif_bytes, file_name)
    
# exif_bytes=piexif.dump(exif_dict)
# im=Image.open("foo.jpg")
# im.thumbnail((100,100),Image.ANTIALIAS)
# im.save("out.jpg",exif=exif_bytes)





  




'''
With Pillow

fromPILimportImage importpiexif im=Image.open(filename) exif_dict=piexif.load(im.info["exif"]) #processimandexif_dict... w,h=im.size exif_dict["0th"][piexif.ImageIFD.XResolution]=(w,1) exif_dict["0th"][piexif.ImageIFD.YResolution]=(h,1) exif_bytes=piexif.dump(exif_dict) im.save(new_file,"jpeg",exif=exif_bytes)







'''

    
'''
Latitude : 35.773713
Longitude: -78.672968
Easting: 710325.92
Northing: 3961357.01
zone: 17S

Here are examples of formats that work:
    Decimal degrees (DD): 41.40338, 2.17403
    Degrees, minutes, and seconds (DMS): 41°24'12.2"N 2°10'26.5"E
    Degrees and decimal minutes (DMM): 41 24.2028, 2 10.4418
'''


'''
piexif There are only just five functions.

- *load(filename)* - Get exif data as *dict*.
- *dump(exif_dict)* - Get exif as *bytes*.
- *insert(exif_bytes, filename)* - Insert exif into JPEG, or WebP.
- *remove(filename)* - Remove exif from JPEG, or WebP.
- *transplant(filename, filename)* - Transplant exif from JPEG to JPEG.

'''
