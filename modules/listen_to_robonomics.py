import logging
import subprocess
import time

from threading import Thread
from modules.send_to_ipfs import send
def listener(config, cams):

    cameras = cams
    program = config['transaction']['path_to_robonomics_file'] + "/robonomics io read launch"
    process = subprocess.Popen(program, shell=True, stdout=subprocess.PIPE)

    logging.warning("Waiting for transaction")
    while True:
        output = process.stdout.readline()
        if output:
            for cam in cameras.keys():
                if (">> " + config['camera' + str(cam)]['address'] + " : true") in output.strip().decode('utf-8'):
                    logging.warning('Transaction to start for ' + cameras[cam].camera_name)
                    start_record_cam_thread = Thread(target=start_record_cam, args=(cameras[cam],))
                    start_record_cam_thread.start()

                elif ('>> ' + config['camera' + str(cam)]['address'] + " : false") in output.strip().decode('utf-8'):
                    logging.warning('Transaction to stop for ' + cameras[cam].camera_name)
                    stop_record_cam(cameras[cam], config)


def start_record_cam(cam):
    if cam.is_busy:
        logging.warning("Camera " + cam.camera_name + " is busy. Record aborted")
        return False
    cam.is_busy = True
    cam.stop_record = False
    cam.record()


def stop_record_cam(cam, config):
    if not cam.is_busy:
        logging.warning("Camera " + cam.camera_name + " is not working yet. Nothing to stop")
    cam.stop_record = True
    send(cam, config)
    cam.is_busy = False
