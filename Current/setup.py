import os

os.system('''
conda create --name conda_bb_env
conda activate conda_bb_env
conda install pip


conda create -n python=3.8 conda_bb_env pip
conda activate conda_bb_env

conda --version
conda create --name conda_bb_env python=3.9
conda activate conda_bb_env


pip install -U pip
cd depthai
python3 install_requirements.py
cd ..
pip freeze > oaksetupwindows.txt
pip3 install -U socketIO-client
pip3 install pathlib2
pip3 install -U paho-mqtt
pip3 install pandas
pip3 install openpyxl
pip3 install pytest-shutil
pip3 install paramiko
pip3 install numpy
pip3 install python-dotenv
pip3 install --upgrade PyQt6
pip freeze > fullsetupwindows.txt
''')