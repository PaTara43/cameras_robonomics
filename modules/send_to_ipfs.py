import ipfshttpclient
import json
import logging
import os
import requests
import subprocess


def send(cam, config):
    if config['ipfs']['enable']:
        try:
            logging.warning('Pushing to IPFS')
            client = ipfshttpclient.connect()
            res = client.add(cam.filename)
            logging.warning('Pushed, hash: ' + res['Hash'])
            _pin_to_temporal(config, cam.filename)
        except Exception as e:
            logging.error("Error while pushing to IPFS, error: ", e)

    if config['general']['delete_after_record']:
        try:
            logging.warning('Removing file')

            os.remove(cam.filename)
        except Exception as e:
            logging.error("Error while deleteng file, error: ", e)

    if config['datalog']['enable']:
        try:
            program = "echo \"" + res['Hash'] + "\" | " + config['transaction']['path_to_robonomics_file'] + "robonomics io write datalog -s " + cam.key
            process = subprocess.Popen(program, shell=True, stdout=subprocess.PIPE)
            output = process.stdout.readline()
            logging.warning("Published data to chain. Transaction hash is " + output.strip().decode('utf8'))
        except Exception as e:
            logging.error("Error while sending IPFS hash to chain, error: ", e)

def _pin_to_temporal(config, file_path: str):
        username = config["temporal"]["temporal_username"]
        password = config["temporal"]["temporal_password"]
        if username and password:
            auth_url = "https://api.temporal.cloud/v2/auth/login"
            token_resp = requests.post(auth_url, json={"username": username, "password": password})
            token = token_resp.json()

            url_add = "https://api.temporal.cloud/v2/ipfs/public/file/add"
            headers = {"Authorization": f"Bearer {token['token']}"}
            resp = requests.post(url_add, files={"file":open(file_path), "hold_time":(None,1)}, headers=headers)

            if resp.status_code == 200:
                logging.warning("File pinned to Temporal Cloud")
