import fnmatch, os, time
import os, os.path
import shutil

def file_rename():
    for file_name in os.listdir('.'):
        time.sleep(1.5)
        t = str(int(time.time()))
        if file_name.startswith('NC_'):
            if file_name.endswith('.JPG'):
                new_name = f"SONY/image_{t}.JPG"
            elif file_name.endswith('.jpg'):
                new_name = f"OAK/image_{t}.jpg"
            os.rename(f"{file_name}", f"{new_name}")
        else:
            continue


def file_move():
    dst_folder1 = os.getcwd()+'/OAK'
    dst_folder2 = os.getcwd()+'/SONY'
    for file_name in os.listdir('.'):
        if file_name.endswith('.JPG'):
            shutil.move(file_name, dst_folder2)
        elif file_name.endswith('.jpg'):
            shutil.move(file_name, dst_folder1)
        else:
            continue


def get_files():
    filelist = [name for name in os.listdir('.') if os.path.isfile(name)]
    count = len(filelist)
    print('File Count:', count)
    for file in filelist:
        os.remove(file)


def list_files():
    # count = len(fnmatch.filter(os.listdir(dir_path), '*.*'))
    files = fnmatch.filter(os.listdir(dir_path), '*.*')
    count = len(files)
    print('File Count:', count)


dir_path = os.getcwd()+'/images'
os.chdir(dir_path)
list_files()
# file_rename()
# file_move()
# get_files()