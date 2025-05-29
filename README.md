# Robotic-Arm-Image-Capture
This is the code for a 2 DOF robotic system that repositions a Raspberry Pi Camera using 2 DC motors controlled with a Raspberry Pi. The system takes pictures simulataneosly. The idea is to capture images of objects from different perspectives for photogrammetry or training object detection algorithms. 

# Introduction

This repository is a thesis work of a robotic system. The system uses a python DC motor control library (documentation can be found in the following repository: https://github.com/dieguelin/Python-DC-Motor-Control-Library-for-Raspberry-Pi ) to control the position of the raspberry pi camera using two DC motors. The code executes a series of camera repositions while simultaneously taking image captures. The exposure time of the camera was reduced to avoid blurry images.

# Getting started

1. Clone repo in desired folder. This must be done inside a Raspberry Pi (guaranteed to work under Raspberry pi 4).
2. Inside the folder, install a virtual environment (see: https://docs.python.org/3/library/venv.html)
3. Activate virtual environment using the command: `source /path/to/env/bin/activate`
4. install RPi.GPIO library using pip command: `pip install RPi.GPIO` (can use alternative package administrator though pip is recommended).
5. Install the picamera module using `pip install picamera` .
6. Can test the motor control library as a module. In source folder, run: `python -m motor_module.motorclass` . This will run code inside `if __name__ == "__main__"`. Alternatively, you can test using the main.py file which direcrtly imports module.

WARNING: Please be careful in choosing the correct GPIO pins. The code won't consider inappropriate GPIO pins. Choosing incorrect GPIO pins can cause unexpected behavior. Consult pin layouts in the raspberry pi documentation: https://www.raspberrypi.com/documentation/computers/ 

# main.py 

The main.py file uses threads to simultaneosly reposition the motor while taking image captures. Threads allow communication between them. Then motor movements are culminated, a signal is sent to the image thread to terminate image captures. The entire process is culminated once both threads finish running.