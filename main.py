import logging
import os
import time
import yaml

from modules.init_cameras import Camera
from modules.listen_to_robonomics import listener
from threading import Thread

def read_configuration(dirname) -> dict:

    config_path = dirname + '/config/config.yaml'
    logging.debug(config_path)

    try:
        with open(config_path) as f:
            content = f.read()
            config = yaml.load(content, Loader=yaml.FullLoader)
            logging.debug(f"Configuration dict: {content}")
            return config
    except Exception as e:
        while True:
            logging.error("Error in configuration file!")
            logging.error(e)
            exit()

class Error(Exception):
    pass


if __name__ == '__main__':
    dirname = os.path.dirname(os.path.abspath(__file__))
    config = read_configuration(dirname)
    cam = Camera(config, dirname)
    logging.warning("Listening to robonomics")
    while True:
        listener(config, cam, dirname)
