import logging
import selectors
import subprocess
import time

from modules.link_to_printer import Task
from modules.send_to_ipfs import send
from modules.url_generator import create_url
from modules.qr_generator import create_qr
from threading import Thread


def listener(config, cam, dirname):

    program_read = config['transaction']['path_to_robonomics_file'] + " io read launch " + config['transaction']['remote']
    process_read = subprocess.Popen("exec " + program_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    sel = selectors.DefaultSelector()
    sel.register(process_read.stdout, selectors.EVENT_READ)
    sel.register(process_read.stderr, selectors.EVENT_READ)

    logging.warning("Waiting for transaction")
    while True:
        for key, _ in sel.select():
            data = key.fileobj.read1(512).decode()
            if not data:
                return False

            elif ("Low open file descriptor limit configured for the process") in data:
                pass

            elif key.fileobj is process_read.stderr:
                logging.warning("Error in listener occurred, rebooting listener")
                process_read.kill()
                time.sleep(2)
                continue

            elif (">> " + config['camera']['address'] + " : true") in data:
                logging.warning('Transaction to start recording')
                if cam.is_busy:
                    logging.warning("Camera is busy. Record aborted")
                    continue
                cam.is_busy = True
                cam.stop_record = False
                start_record_cam_thread = Thread(target=start_record_cam, args=(cam, dirname,))
                start_record_cam_thread.start()
                create_url_r_thread = Thread(target=create_url_r, args=(cam, dirname, config,))
                create_url_r_thread.start()

            elif (">> " + config['camera']['address'] + " : false") in data:
                logging.warning('Transaction to stop recording')
                if not cam.is_busy:
                    logging.warning("Camera is not recording. Nothing to stop")
                    continue
                cam.stop_record = True
                cam.is_busy = False
                try:
                    stop_record_cam_thread = Thread(target=stop_record_cam, args=(cam.filename, cam.keyword, cam.qrpic, config, dirname,))
                    stop_record_cam_thread.start()
                except Exception as e:
                    cam.process_ffmpeg.communicate(input = b'q')[0]
                    logging.warning("Stoped recording image at Exception")
                    time.sleep(1)
                    self.process_ffmpeg.kill()

def start_record_cam(cam, dirname):
    cam.record(dirname)


def stop_record_cam(filename, keyword, qrpic, config, dirname):
    time.sleep(1)
    send(filename, keyword, qrpic, config, dirname)


def create_url_r(cam, dirname, config):
    cam.keyword, cam.link = create_url(config)
    logging.warning(cam.link)
    cam.qrpic = create_qr(dirname, cam.link)
    if config['print_qr']['enable']:
        printer = Task(cam.qrpic)
