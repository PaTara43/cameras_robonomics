import logging
import subprocess
import time

from threading import Thread
from modules.send_to_ipfs import send
from modules.url_generator import create_url
# from modules.link_to_printer import Task

def listener(config, cam):

    program_read = config['transaction']['path_to_robonomics_file'] + " io read launch"
    process_read = subprocess.Popen("exec " + program_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    bug_catcher = Thread(target=catch_bugs, args=(config, cam, process_read))
    bug_catcher.start()

    logging.warning("Waiting for transaction")
    while True:
        output = process_read.stdout.readline()
        if output:
            if (">> " + config['camera']['address'] + " : true") in output.strip().decode('utf-8'):
                logging.warning('Transaction to start recording')
                start_record_cam_thread = Thread(target=start_record_cam, args=(cam,))
                start_record_cam_thread.start()
                create_url_r_thread = Thread(target=create_url_r, args=(cam,))
                create_url_r_thread.start()
            elif ('>> ' + config['camera']['address'] + " : false") in output.strip().decode('utf-8'):
                logging.warning('Transaction to stop recording')
                stop_record_cam_thread = Thread(target=stop_record_cam, args=(cam,config,))
                stop_record_cam_thread.start()



def start_record_cam(cam):
    if cam.is_busy:
        logging.warning("Camera is busy. Record aborted")
        return False
    cam.is_busy = True
    cam.stop_record = False
    cam.record()


def stop_record_cam(cam, config):
    if not cam.is_busy:
        logging.warning("Camera is not recording yet. Nothing to stop")
    cam.stop_record = True
    time.sleep(1)
    send(cam, config)
    cam.is_busy = False


def catch_bugs(config, cam, process_read):
    error = process_read.stderr.readline()
    if error:
        logging.warning("Error in listener occurred, rebooting listener")
        process_read.kill()
        time.sleep(2)
        listener(config, cam)


def create_url_r(cam):
    cam.keyword, cam.link = create_url()
    #Task.send_task_to_printer(cam.link)
