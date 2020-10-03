import logging
import subprocess
import time

from threading import Thread

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
                    if config['general']['mode'] == 'stream':
                        start_stream_cam_thread = Thread(target=start_stream_cam, args=(cameras[cam],))
                        start_stream_cam_thread.start()
                    elif config['general']['mode'] == 'record':
                        start_record_cam_thread = Thread(target=start_record_cam, args=(cameras[cam],))
                        start_record_cam_thread.start()

                elif ('>> ' + config['camera' + str(cam)]['address'] + " : false") in output.strip().decode('utf-8'):
                    logging.warning('Transaction to stop for ' + cameras[cam].camera_name)
                    if config['general']['mode'] == 'stream':
                        stop_stream_cam(cameras[cam])
                    elif config['general']['mode'] == 'record':
                        stop_record_cam(cameras[cam])

def start_stream_cam(cam):
    if cam.is_busy:
        logging.warning("Camera " + cam.camera_name + " is busy. Stream aborted")
        return False
    cam.is_busy = True
    cam.stop_stream = False

    #Заглушка
    while True and not cam.stop_stream:
        print("camera " + cam.camera_name + " is streaming")
        time.sleep(1)

    # cam.stream()


def stop_stream_cam(cam):
    if not cam.is_busy:
        logging.warning("Camera " + cam.camera_name + " is not working yet. Nothing to stop")
    cam.stop_stream = True
    cam.is_busy = False


def start_record_cam(cam):
    if cam.is_busy:
        logging.warning("Camera " + cam.camera_name + " is busy. Record aborted")
        return False
    cam.is_busy = True
    cam.stop_record = False

    #Заглушка
    while True and not cam.stop_record:
        print("camera " + cam.camera_name + " is recording")
        time.sleep(1)

    # cam.record()


def stop_record_cam(cam):
    if not cam.is_busy:
        logging.warning("Camera " + cam.camera_name + " is not working yet. Nothing to stop")
    cam.stop_record = True
    cam.is_busy = False
