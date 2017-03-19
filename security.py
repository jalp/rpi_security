#!usr/bin/env python

import os
import subprocess
import RPi.GPIO as GPIO
from picamera import PiCamera
from datetime import datetime
from time import sleep

GPIO.setmode(GPIO.BCM)
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

directory = '/home/pi/projects/security/cam/'

if not os.path.exists(directory):
    os.makedirs(directory)

print('Starting...')


def callback(PIR_PIN):
    send_message(take_picture())


def take_picture():
    print('Taking picture...')
    file_date = datetime.now().strftime("%Y-%m-%d-%H:%M")
    with PiCamera() as picam:
        picam.start_preview()
        picam.annotate_text_size = 20
        picam.annotate_text = '{0}'.format(datetime.now().strftime('%c'))
        sleep(2)
        picam.capture('{0}/image{1}.jpg'.format(directory, file_date))
        picam.stop_preview()
        print('Recording video')
        picam.start_recording('{0}video{1}.h264'.format(directory, file_date))
        sleep(10)
        picam.stop_recording()
        picam.close()
    return file_date


def send_message(file_date):
    telegram = subprocess.Popen(
        ['telegram-cli', '--wait-dialog-list', '--disable-link-preview', '--disable-colors', '--disable-readline'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        bufsize=1, shell=True)
    print('Telegram started')
    sleep(2)
    print('Sending message')
    command = 'msg Jalp Movimiento en casa!!!'
    telegram.stdin.write('{0}\n'.format(command).encode('utf-8'))
    telegram.stdin.flush()

    print('Message sent! Closing telegram')
    telegram.stdin.write('quit\n'.encode('utf-8'))
    telegram.stdin.flush()

    print('Sending photo')
    subprocess.Popen(['./telegram_send_image.sh', '{0}/image{1}.jpg'.format(directory, file_date)])


try:
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=callback, bouncetime=200)
    print('Waiting for movement')
    while True:
        sleep(15)
except KeyboardInterrupt:
    print('Exit')
    GPIO.cleanup()
