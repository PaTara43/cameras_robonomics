import logging
import qrcode
import subprocess
import time

from modules.link_to_printer import Task
from modules.send_to_ipfs import send
from modules.url_generator import create_url
from PIL import Image
from threading import Thread


def listener(config, cam, dirname):

    program_read = config['transaction']['path_to_robonomics_file'] + " io read launch --remote " + config['transaction']['remote']
    process_read = subprocess.Popen("exec " + program_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    bug_catcher = Thread(target=catch_bugs, args=(config, cam, process_read, dirname,))
    bug_catcher.start()

    logging.warning("Waiting for transaction")
    while True:
        output = process_read.stdout.readline()
        if output:
            if (">> " + config['camera']['address'] + " : true") in output.strip().decode('utf-8'):
                logging.warning('Transaction to start recording')
                start_record_cam_thread = Thread(target=start_record_cam, args=(cam,))
                start_record_cam_thread.start()
                create_url_r_thread = Thread(target=create_url_r, args=(cam, dirname,))
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
        return False
    cam.stop_record = True
    time.sleep(1)
    send(cam, config)
    cam.is_busy = False


def catch_bugs(config, cam, process_read, dirname):
    error = process_read.stderr.readline()
    if error:
        logging.warning("Error in listener occurred, rebooting listener")
        process_read.kill()
        time.sleep(2)
        listener(config, cam, dirname)


def create_url_r(cam, dirname):
    cam.keyword, cam.link = create_url()
    logging.warning(cam.link)

    robonomics = Image.open(dirname + '/modules/robonomics.jpg').resize((100,100))
    qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr_big.add_data('https://'+cam.link)
    qr_big.make()
    img_qr_big = qr_big.make_image().convert('RGB')

    pos = ((img_qr_big.size[0] - robonomics.size[0]) // 2, (img_qr_big.size[1] - robonomics.size[1]) // 2)

    img_qr_big.paste(robonomics, pos)
    cam.qrpic = cam.output_dir + 'qr.png'
    img_qr_big.save(cam.qrpic)
    printer = Task()
    printer.send_task_to_printer(cam.qrpic)
