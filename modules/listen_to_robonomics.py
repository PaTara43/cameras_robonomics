import logging
import sys
import time
from threading import Thread

import RPi.GPIO as GPIO

from modules.init_cameras import Camera
from modules.link_to_printer import Task
from modules.qr_generator import create_qr
from modules.send_to_ipfs import send
from modules.url_generator import create_url


def listener(channel: int, config: dict, cam: Camera, dirname: str) -> None:

    time.sleep(0.1)
    if not GPIO.input(channel):
        if cam.initial_launch:
            cam.initial_launch = False
        if cam.is_busy:
            logging.warning("Camera is busy. Record aborted")
            return None
        cam.stop_record = False
        cam.is_busy = True
        start_record_cam_thread = Thread(
            target=start_record_cam,
            args=(
                cam,
                dirname,
            ),
        )
        start_record_cam_thread.start()
        create_url_r_thread = Thread(
            target=create_url_r,
            args=(
                cam,
                dirname,
                config,
            ),
        )
        create_url_r_thread.start()

    else:
        if cam.initial_launch:
            cam.initial_launch = False
            return None
        if not cam.is_busy:
            logging.warning("Camera is not recording. Nothing to stop")
            return None
        cam.stop_record = True
        cam.is_busy = False
        stop_record_cam_thread = Thread(
            target=stop_record_cam,
            args=(
                cam.filename,
                cam.keyword,
                cam.qrpic,
                config,
                dirname,
            ),
        )
        stop_record_cam_thread.start()


def start_record_cam(cam: Camera, dirname: str) -> None:
    cam.record(dirname)
    sys.exit()


def stop_record_cam(filename: str, keyword: str, qrpic: str, config: dict, dirname: str) -> None:
    time.sleep(1)
    send(filename, keyword, qrpic, config, dirname)
    sys.exit()


def create_url_r(cam: Camera, dirname: str, config: dict) -> None:
    cam.keyword, cam.link = create_url(config)
    logging.warning(cam.link)
    cam.qrpic = create_qr(dirname, cam.link, config)
    if config["print_qr"]["enable"]:
        Task(cam.qrpic)
