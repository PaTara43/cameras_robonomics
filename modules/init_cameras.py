import cv2
import logging
import time
import subprocess

from threading import Thread


class Camera():


    def __init__(self, config):

        self.ip = config['camera']['ip']
        self.port = config['camera']['port']
        self.login = config['camera']['login']
        self.password = config['camera']['password']
        self.camera_address = config['camera']['address']
        self.key = config['camera']['key']
        self.framerate = config['camera']['framerate']
        self.output_dir = config['general']['output_dir']

        self.is_busy = False
        self.stop_stream = False
        self.stop_record = False

    def record(self):

        self.filename = time.ctime(time.time()).replace(" ", "_") + '.mp4'
        self.program_ffmpeg= 'ffmpeg -loglevel debug -rtsp_transport tcp -i "rtsp://' + self.login + ':' + self.password + '@' + self.ip \
            + ':' + self.port + '/Streaming/Channels/101" -c copy -map 0 ' + self.filename
        self.process_ffmpeg = subprocess.Popen("exec " + self.program_ffmpeg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        logging.warning("Started recording image")
        while not self.stop_record:
            continue
        self.process_ffmpeg.communicate(input = b'q')[0]
        logging.warning("Stoped recording image")
        time.sleep(1)
        self.process_ffmpeg.kill()
