'''
Project logger
'''

from datetime import date
import time
import cv2
from pathlib import Path
from from_root import from_root, from_here
import csv
import os, sys
from datetime import datetime
import json
# imports for image logging
import piexif
from fractions import Fraction

'''
    Camera Status Logging Function
'''
img_log_dir = from_here("images_log")
cam_log_dir = from_here("camera_log")
# img_log_dir = Path("images_log")
# cam_log_dir = Path("camera_log")

Path(img_log_dir).mkdir(parents=True, exist_ok=True)
Path(cam_log_dir).mkdir(parents=True, exist_ok=True)

# if csv file doesn't exist, create one
cam_status_file = cam_log_dir / "camera_status.csv"
fields = ['Timestamp', 'Connected', 'NotConnected']
if not cam_status_file.exists():
    print("Camera Status file doesn't exist")
    with open(cam_status_file, 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writeheader()


# writing current camera status to the csv file ( takes < 3 ms )
def system_camera_status():
    # st = time.time()
    camera_dict = [{'Timestamp': None, 'Connected': [], 'NotConnected': []} ]
    json_files = [cam_json for cam_json in os.listdir(cam_log_dir) if cam_json.endswith('.json')]
    # print(json_files)
    
    for cam_file in json_files:
        with open(cam_log_dir / cam_file) as json_file:
            data = json.load(json_file)
            if data['Status'] == 'Connected':
                camera_dict[0]['Connected'].append(data['Camera_ID'])
            else:
                camera_dict[0]['NotConnected'].append(data['Camera_ID'])
    camera_dict[0]['Timestamp'] = datetime.utcnow()
    camera_dict[0]['Connected'].sort()
    camera_dict[0]['NotConnected'].sort()
    # print(camera_dict)

    with open(cam_status_file, 'a', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writerows(camera_dict)
    # et = time.time()
    # elapsed_time = (et - st)*1000
    # print('CSV Execution time:', elapsed_time)

    print("----- Current System Status -----")
    print("Connected Cameras:", camera_dict[0]['Connected'])
    print("Disconnected Cameras:", camera_dict[0]['NotConnected'])

# takes around 3 ms max, mostly < 1 ms
def camera_status_log(cam_id, status):
    # st = time.time()
    camera_dict = {'Camera_ID': cam_id, 'Timestamp': str(datetime.utcnow()), 'Status': status}
    fileName = f"{cam_log_dir}/Camera_{cam_id}.json"
    # print(fileName)

    with open(fileName, 'w') as fp:
        json.dump(camera_dict, fp)
    # et = time.time()
    # elapsed_time = (et - st)*1000
    # print('Execution time:', elapsed_time)
    

# camera_status_log(1, 'Connected')
# camera_status_log(2, 'Connected')
# camera_status_log(3, 'NotConnected')
# camera_status_log(4, 'Connected')
# camera_status_log(5, 'Connected')
# camera_status_log(6, 'NotConnected')
# camera_status_log(7, 'NotConnected')
# camera_status_log(8, 'Connected')
# system_camera_status()



'''
    Images Logging function
'''

# if csv file doesn't exist, create one
img_log_file = img_log_dir / "images_log.csv"
i_fields = ['Timestamp', 'Image Name', 'GPS']
if not img_log_file.exists():
    print("Image log file doesn't exist")
    with open(img_log_file, 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = i_fields)
        writer.writeheader()


def log_image(img, img_type, gps_tag):
    # save image in the image log directory
    date_obj = datetime.utcnow()
    day = date_obj.date()
    hour = date_obj.time().hour
    minutes = date_obj.time().minute
    imgName = f"{day}_{hour}:{minutes}_{img_type}.jpg"
    fileName = f"{img_log_dir}/{imgName}"
    cv2.imwrite(fileName, img)

    # add gps tags to the saved image
    lat = dd_to_dms(gps_tag[0])
    lng = dd_to_dms(gps_tag[1])
    if gps_tag[0]<0:    lat_ref = 'S'
    else:   lat_ref = 'N'
    if gps_tag[1]<0:    lng_ref = 'W'
    else:   lng_ref = 'E'

    exiv_lat = (to_rational(lat[0]), to_rational(lat[1]), to_rational(lat[2]))
    exiv_lng = (to_rational(lng[0]), to_rational(lng[1]), to_rational(lng[2]))
    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSLatitudeRef: lat_ref,
        piexif.GPSIFD.GPSLatitude: exiv_lat,
        piexif.GPSIFD.GPSLongitudeRef: lng_ref,
        piexif.GPSIFD.GPSLongitude: exiv_lng,
    }
    exif_dict = {"GPS": gps_ifd}
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, fileName)
    
    # log gps tag with image name in the csv file
    img_dict = [{'Timestamp': datetime.utcnow(), 'Image Name': imgName, 'GPS': gps_tag} ]
    with open(img_log_file, 'a', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = i_fields)
        writer.writerows(img_dict)

'''
convert decimal degree to degrees, munutes and seconds
arguments: gps-coordinates latitude or longitude e.g. 35.773713
return: gps-coordinates in DMS (35, 46, 25.3668)
'''
def dd_to_dms(coordinate):
    coordinate = abs(coordinate)
    deg = int(coordinate)
    min_sec = (coordinate - deg) * 60
    min = int(min_sec)
    sec = round((min_sec - min) * 60, 5)
    return (deg, min, sec)

'''
convert integer values to fractions which is the format acceptable by exif for degrees, minutes and seconds
arguments: 25.3668
return: (63417, 2500)
'''
def to_rational(val):
    f = Fraction(str(val))
    return (f.numerator, f.denominator)
  


    
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

# im = Image.open(fileName)
# im.save(fileName, 'jpeg', exif=exif_bytes)
'''
