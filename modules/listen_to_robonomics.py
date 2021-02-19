import RPi.GPIO as GPIO
import logging
import selectors
import sys
import subprocess
import time

from modules.link_to_printer import Task
from modules.send_to_ipfs import send
from modules.url_generator import create_url
from modules.qr_generator import create_qr
from threading import Thread


def listener(channel, config, cam, dirname):

    time.sleep(0.1)
    if not GPIO.input(channel):
        if cam.initial_launch:
            cam.initial_launch = False
        if cam.is_busy:
            logging.warning("Camera is busy. Record aborted")
            return False
        cam.stop_record = False
        cam.is_busy = True
        start_record_cam_thread = Thread(target=start_record_cam, args=(cam, dirname,))
        start_record_cam_thread.start()
        create_url_r_thread = Thread(target=create_url_r, args=(cam, dirname, config,))
        create_url_r_thread.start()

    else:
        if cam.initial_launch:
            cam.initial_launch = False
            return False
        if not cam.is_busy:
            logging.warning("Camera is not recording. Nothing to stop")
            return False
        cam.stop_record = True
        cam.is_busy = False
        stop_record_cam_thread = Thread(target=stop_record_cam, args=(cam.filename, cam.keyword, cam.qrpic, config, dirname,))
        stop_record_cam_thread.start()

def start_record_cam(cam, dirname):
    cam.record(dirname)
    sys.exit()

def stop_record_cam(filename, keyword, qrpic, config, dirname):
    time.sleep(1)
    send(filename, keyword, qrpic, config, dirname)
    sys.exit()

def create_url_r(cam, dirname, config):
    cam.keyword, cam.link = create_url(config)
    logging.warning(cam.link)
    cam.qrpic = create_qr(dirname, cam.link)
    if config['print_qr']['enable']:
        printer = Task(cam.qrpic)
