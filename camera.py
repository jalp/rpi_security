#!usr/bin/env python

import os
from picamera import PiCamera
from time import sleep

directory = '/home/pi/projects/security/cam/'

if not os.path.exists(directory):
    os.makedirs(directory)

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.capture('{0}/image.jpg'.format(directory))
camera.stop_preview()
