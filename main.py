import logging
import os
import time
import yaml

from modules.init_cameras import Camera
from modules.listen_to_robonomics import listener
from threading import Thread

def read_configuration() -> dict:

    config_path = dirname + '/config/config.yaml'
    logging.debug(config_path)

    try:
        with open(config_path) as f:
            content = f.read()
            config = yaml.load(content, Loader=yaml.FullLoader)
            logging.debug(f"Configuration dict: {content}")
            if not os.path.exists(config['general']['output_dir']):
                raise Error("Output folder " + config['general']['output_dir'] + " doesn't exist! Create it or edit config file.")
            return config
    except Exception as e:
        while True:
            logging.error("Error in configuration file!")
            logging.error(e)
            exit()


def listen_to_robonomics_func(config, cams):

    logging.warning("Listening to robonomics")
    listener(config, cams)


if __name__ == '__main__':
    dirname = os.path.dirname(os.path.abspath(__file__))
    config = read_configuration()

    cams = {}
    try:
        for i in range(config['general']['num_cams']):
            if config['camera'+str(i)]['enable']:
                cams[i] = Camera(i, config)
    except KeyError:
        logging.error("Number of cameras in config file doesn't match cameras' parameters blocks")
        exit()
    listen_to_robonomics_func(config, cams)
