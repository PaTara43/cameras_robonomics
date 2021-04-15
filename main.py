import asyncio
import RPi.GPIO as GPIO
import logging
import os
import time
import yaml

from modules.init_cameras import Camera
from modules.listen_to_robonomics import listener
from threading import Thread


def read_configuration(dirname_f) -> dict:

    config_path = dirname_f + "/config/config.yaml"
    logging.debug(config_path)

    try:
        with open(config_path) as f:
            content = f.read()
            config_f = yaml.load(content, Loader=yaml.FullLoader)
            logging.debug(f"Configuration dict: {content}")
            return config_f
    except Exception as e:
        while True:
            logging.error("Error in configuration file!")
            logging.error(e)
            exit()


class Error(Exception):
    pass


if __name__ == "__main__":
    dirname = os.path.dirname(os.path.abspath(__file__))
    config = read_configuration(dirname)
    cam = Camera(config)
    cam.initial_launch = True
    cam.is_busy = False
    channel = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(
        channel,
        GPIO.BOTH,
        callback=lambda x: listener(channel, config, cam, dirname),
        bouncetime=1000,
    )  # Setup event on pin 12 rising edge
    loop = asyncio.get_event_loop()
    loop.run_forever()
    print("Waiting for button to be pressed")  # Run until someone presses enter

    GPIO.cleanup()  # Clean up
