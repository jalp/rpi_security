#!usr/bin/env python

import os
import subprocess
import logging
import RPi.GPIO as GPIO
from picamera import PiCamera
from datetime import datetime
from time import sleep

LOG_LEVEL = logging.INFO
LOG_FILE = '/home/pi/logs/security.log'
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)

GPIO.setmode(GPIO.BCM)
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

directory = '/home/pi/projects/security/cam/'

if not os.path.exists(directory):
    os.makedirs(directory)


def callback(PIR_PIN):
    send_message(take_picture())


def take_picture():
    logging.info('Taking picture...')
    file_date = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    with PiCamera() as picam:
        picam.rotation = 180
        picam.start_preview()
        picam.annotate_text_size = 20
        picam.annotate_text = '{0}'.format(datetime.now().strftime('%c'))
        sleep(2)
        picam.capture('{0}image{1}.jpg'.format(directory, file_date))
        picam.stop_preview()
        logging.info('Recording video')
        picam.start_recording('{0}video{1}.h264'.format(directory, file_date))
        sleep(10)
        picam.stop_recording()
        picam.close()
    return file_date


def send_message(file_date):
    command = 'msg Jalp Movimiento en casa!!!'
    subprocess.Popen(['telegram-cli',
                      '--log-level', '0',
                      '--verbosity', '0',
                      '--wait-dialog-list',
                      '--disable-link-preview',
                      '--disable-colors',
                      '--disable-readline',
                      '--disable-output',
                      '--exec', '{0}'.format(command.replace('\n', '\\n'))],
                     stdout=subprocess.PIPE)
    sleep(1)

    text = '{0}image{1}.jpg'.format(directory, file_date)
    subprocess.Popen(['telegram-cli',
                      '--log-level', '0',
                      '--verbosity', '0',
                      '--wait-dialog-list',
                      '--disable-link-preview',
                      '--disable-colors',
                      '--disable-readline',
                      '--disable-output',
                      '--exec', 'send_photo Jalp "{0}"'.format(text.replace('\n', '\\n'))],
                     stdout=subprocess.PIPE)


try:
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=callback, bouncetime=200)
    logging.info('Waiting for movement')
    while True:
        sleep(15)
except KeyboardInterrupt:
    logging.info('Exit')
    GPIO.cleanup()
