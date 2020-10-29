import ipfshttpclient
import json
import logging
import os
import requests
import subprocess

from pinatapy import PinataPy


def send(cam, config):
    logging.warning("Camera " + cam.camera_name + ' sending file to pinata')

    if config['pinata']['enable']:
        try:
            hash = _pin_to_pinata(cam, config)
        except Exception as e:
            logging.error("Camera " + cam.camera_name + " Error while pinning to pinata, error: ", e)

    if config['general']['delete_after_record']:
        try:
            logging.warning("Camera " + cam.camera_name + ' Removing file')

            os.remove(cam.filename)
        except Exception as e:
            logging.error("Camera " + cam.camera_name + " Error while deleteng file, error: ", e)

    if config['datalog']['enable']:
        try:
            program = "echo \"" + hash + "\" | " + config['transaction']['path_to_robonomics_file'] + "robonomics io write datalog -s " + cam.key
            process = subprocess.Popen(program, shell=True, stdout=subprocess.PIPE)
            output = process.stdout.readline()
            logging.warning("Camera " + cam.camera_name + " Published data to chain. Transaction hash is " + output.strip().decode('utf8'))
        except Exception as e:
            logging.error("Camera " + cam.camera_name + " Error while sending IPFS hash to chain, error: ", e)


def _pin_to_pinata(cam, config):
        pinata_api = config["pinata"]["pinata_api"]
        pinata_secret_api = config["pinata"]["pinata_secret_api"]
        if pinata_api and pinata_secret_api:
            pinata = PinataPy(pinata_api, pinata_secret_api)
            pinata.pin_file_to_ipfs(cam.filename)
            logging.warning("Camera " + cam.camera_name + " Pinata hash is " + pinata.pin_list()['rows'][0]['ipfs_pin_hash'])
            return pinata.pin_list()['rows'][0]['ipfs_pin_hash']
