import ipfshttpclient
import logging
import os
import subprocess


def send(cam, config):
    if config['ipfs']['enable']:
        try:
            logging.warning('Pushing to IPFS')
            client = ipfshttpclient.connect()
            res = client.add(cam.filename)
            logging.warning('Pushed, hash: ' + res['Hash'])
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
            program = "echo \"" + res['Hash'] + "\" | " + config['transaction']['path_to_robonomics_file'] + "/robonomics io write datalog -s " + cam.key
            process = subprocess.Popen(program, shell=True, stdout=subprocess.PIPE)
            output = process.stdout.readline()
            # print(output.strip())
            logging.warning("Published data to chain. Transaction hash is " + output.strip().decode('utf8'))
        except Exception as e:
            logging.error("Error while sending IPFS hash to chain, error: ", e)
