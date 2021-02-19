import RPi.GPIO as GPIO
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
    cam.initial_launch = True

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(18,GPIO.BOTH,callback=listener(18, config, cam, dirname), bouncetime=1000) # Setup event on pin 12 rising edge

    input("Waiting for button to be pressed") # Run until someone presses enter
    GPIO.cleanup() # Clean up
