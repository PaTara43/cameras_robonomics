import glob
import ipfshttpclient
import json
import logging
import os
import requests
import subprocess
import time


from pinatapy import PinataPy
from modules.url_generator import update_url


def send(filename, keyword, qrpic, config, dirname):

    if config['intro']['enable']:
        try:
            logging.warning("Concatenating videos")
            if not os.path.exists(dirname + "/media/intro.mp4"):
                raise Error("Intro file doesn't exist!")
            concat_string = "file \'" + dirname + "/media/intro.mp4\'\nfile \'" + filename + "\'"
            with open(dirname + "/output/vidlist.txt", "w") as text_file:
                text_file.write(concat_string)
            text_file.close()
            concat_filename = filename[:-4] + '_intro' + filename[-4:]
            concat_command = "ffmpeg -f concat -safe 0 -i " + dirname + "/output/vidlist.txt -c copy " + concat_filename
            concat_process = subprocess.Popen("exec " + concat_command,\
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            res = concat_process.stdout.readline()
        except Exception as e:
            logging.error("Error while concatenating videos: ", e)
    if config['ipfs']['enable']:
        try:
            logging.warning("Camera is publishing file to IPFS")
            client = ipfshttpclient.connect()
            if config['intro']['enable']:
                res = client.add(concat_filename)
            else:
                res = client.add(filename)
            hash = res['Hash']
            logging.warning('Published to IPFS, hash: ' + hash)
            if hash:
                try:
                    logging.warning("Updating URL")
                    update_url(keyword, hash, config)
                except Exception as e:
                    logging.error("Error while updating URL, error: ", e)
        except Exception as e:
            logging.error("Error while publishing to IPFS, error: ", e)

    if config['pinata']['enable']:
        try:
            logging.warning("Camera is sending file to pinata")

            if config['intro']['enable']:
                hash_pinata = _pin_to_pinata(concat_filename, config)
            else:
                hash_pinata = _pin_to_pinata(filename, config)

        except Exception as e:
            logging.error("Error while pinning to pinata, error: ", e)

    if config['general']['delete_after_record']:
        try:
            logging.warning('Removing files')
            os.remove(filename)
            os.remove(qrpic)
            if config['intro']['enable']:
                os.remove(concat_filename)
        except Exception as e:
            logging.error("Error while deleteng file, error: ", e)

    if config['datalog']['enable']:
        try:
            program = "echo \"" + hash + "\" | " + config['transaction']['path_to_robonomics_file'] + "\
             io write datalog " + config['transaction']['remote'] + " -s " + config['camera']['key']
            process = subprocess.Popen(program, shell=True, stdout=subprocess.PIPE)
            output = process.stdout.readline()
            logging.warning("Published data to chain. Transaction hash is " + output.strip().decode('utf8'))
        except Exception as e:
            logging.error("Error while sending IPFS hash to chain, error: ", e)


def _pin_to_pinata(filename, config):
    pinata_api = config["pinata"]["pinata_api"]
    pinata_secret_api = config["pinata"]["pinata_secret_api"]
    if pinata_api and pinata_secret_api:
        pinata = PinataPy(pinata_api, pinata_secret_api)
        pinata.pin_file_to_ipfs(filename)
        logging.warning("File sent")
        return pinata.pin_list()['rows'][0]['ipfs_pin_hash']
