import logging
import qrcode
import selectors
import subprocess
import time

from modules.link_to_printer import Task
from modules.send_to_ipfs import send
from modules.url_generator import create_url
from PIL import Image
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
                if config['print_qr']['enable']:
                    create_url_r_thread = Thread(target=create_url_r, args=(cam, dirname, config,))
                    create_url_r_thread.start()

            elif (">> " + config['camera']['address'] + " : false") in data:
                logging.warning('Transaction to stop recording')
                if not cam.is_busy:
                    logging.warning("Camera is not recording. Nothing to stop")
                    continue
                cam.stop_record = True
                cam.is_busy = False
                stop_record_cam_thread = Thread(target=stop_record_cam, args=(cam.filename, cam.keyword, cam.qrpic, config, dirname,))
                stop_record_cam_thread.start()


def start_record_cam(cam, dirname):
    cam.record(dirname)


def stop_record_cam(filename, keyword, qrpic, config, dirname):
    time.sleep(1)
    send(filename, keyword, qrpic, config, dirname)


def create_url_r(cam, dirname, config):
    cam.keyword, cam.link = create_url(config)
    logging.warning(cam.link)

    robonomics = Image.open(dirname + '/media/robonomics.jpg').resize((100,100))
    qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr_big.add_data('https://'+cam.link)
    qr_big.make()
    img_qr_big = qr_big.make_image().convert('RGB')

    pos = ((img_qr_big.size[0] - robonomics.size[0]) // 2, (img_qr_big.size[1] - robonomics.size[1]) // 2)

    img_qr_big.paste(robonomics, pos)
    cam.qrpic = dirname + "/output/" + time.ctime(time.time()).replace(" ", "_") + 'qr.png'
    img_qr_big.save(cam.qrpic)
    printer = Task()
    printer.send_task_to_printer(cam.qrpic)
