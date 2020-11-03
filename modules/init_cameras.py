import cv2
import logging
import time
import subprocess

from threading import Thread


class Camera():


    def __init__(self, camera_no, config):

        self.camera_name = 'cam' + str(camera_no)
        self.ip = config['camera'+str(camera_no)]['ip']
        self.port = config['camera'+str(camera_no)]['port']
        self.login = config['camera'+str(camera_no)]['login']
        self.password = config['camera'+str(camera_no)]['password']
        self.camera_address = config['camera'+str(camera_no)]['address']
        self.key = config['camera'+str(camera_no)]['key']
        self.framerate = config['camera'+str(camera_no)]['framerate']
        self.output_dir = config['general']['output_dir']

        self.is_busy = False
        self.stop_stream = False
        self.stop_record = False

    def record(self):

        self.filename = self.camera_name + '_' + time.ctime(time.time()).replace(" ", "_") + '.mp4'
        self.program_ffmpeg= 'ffmpeg -loglevel debug -rtsp_transport tcp -i "rtsp://' + self.login + ':' + self.password + '@' + self.ip \
            + ':' + self.port + '/Streaming/Channels/101" -c copy -map 0 ' + self.filename
        self.process_ffmpeg = subprocess.Popen("exec " + self.program_ffmpeg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        logging.warning("Started recording image from " + self.camera_name)
        while not self.stop_record:
            continue
        self.process_ffmpeg.communicate(input = b'q')[0]
        # self.process_ffmpeg.kill()
        logging.warning("Stoped recording image from " + self.camera_name)
