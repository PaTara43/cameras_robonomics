import ipfshttpclient
import json
import logging
import os
import requests
import subprocess

from pinatapy import PinataPy
from modules.url_generator import update_url


def send(cam, config):

    if config['ipfs']['enable']:
        try:
            logging.warning("Camera is publishing file to IPFS")
            client = ipfshttpclient.connect()
            res = client.add(cam.filename)
            hash = res['Hash']
            logging.warning('Published to IPFS, hash: ' + hash)
        except Exception as e:
            logging.error("Error while publishing to IPFS, error: ", e)


    if config['pinata']['enable']:
        try:
            logging.warning("Camera is pinning hash to pinata")
            hash_pinata = _pin_to_pinata(hash, config)
        except Exception as e:
            logging.error("Error while pinning to pinata, error: ", e)

    if hash:
        try:
            logging.warning("Updating URL")
            update_url(cam.keyword, hash)
        except Exception as e:
            logging.error("Error while updating URL, error: ", e)

    if config['general']['delete_after_record']:
        try:
            logging.warning('Removing file')
            os.remove(cam.filename)
            os.remove(cam.qrpic)
        except Exception as e:
            logging.error("Error while deleteng file, error: ", e)

    if config['datalog']['enable']:
        try:
            program = "echo \"" + hash + "\" | " + config['transaction']['path_to_robonomics_file'] + "\
             io write datalog --remote " + config['transaction']['remote'] + " -s " + cam.key
            process = subprocess.Popen(program, shell=True, stdout=subprocess.PIPE)
            output = process.stdout.readline()
            logging.warning("Published data to chain. Transaction hash is " + output.strip().decode('utf8'))
        except Exception as e:
            logging.error("Error while sending IPFS hash to chain, error: ", e)


def _pin_to_pinata(hash, config):
        pinata_api = config["pinata"]["pinata_api"]
        pinata_secret_api = config["pinata"]["pinata_secret_api"]
        if pinata_api and pinata_secret_api:
            pinata = PinataPy(pinata_api, pinata_secret_api)
            pinata.add_hash_to_pin_queue(hash)
            logging.warning("Hash added to pin queue")
            return pinata.pin_list()['rows'][0]['ipfs_pin_hash']
