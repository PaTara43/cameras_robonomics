import cv2
import logging
import time

from threading import Thread


class Camera():


    def __init__(self, camera_no, config):

        self.camera_name = 'cam' + str(camera_no)
        self.ip = config['camera'+str(camera_no)]['ip']
        self.port = config['camera'+str(camera_no)]['port']
        self.login = config['camera'+str(camera_no)]['login']
        self.password = config['camera'+str(camera_no)]['password']
        self.camera_address = config['camera'+str(camera_no)]['address']
        self.framerate = config['camera'+str(camera_no)]['framerate']
        self.output_dir = config['general']['output_dir']

        self.is_busy = False
        self.stop_stream = False
        self.stop_record = False


    def connect(self) -> bool:

        logging.warning("Connecting to " + self.camera_name)

        try:
            # TODO: timeout
            self.cap = cv2.VideoCapture('rtsp://'+ self.login + ':' + self.password + '@' + self.ip + ':' + self.port + '/Streaming/Channels/101')
            logging.warning("Capturing image from  " + self.camera_name)
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.connected = True


        except Exception as e:
            logging.error("Failed to connect to " + self.camera_name + '. \nError: ' + e)
            self.connected = False


    def record(self):

        try:
            self.connect()
            if self.connected:
                logging.warning("Started recording image from " + self.camera_name)
                self.out = cv2.VideoWriter(self.output_dir + 'video_' + self.camera_name + '_' + time.ctime(time.time()).replace(" ", "_") + '.avi',\
                    self.fourcc, self.framerate, (self.width,self.height))
                while self.cap.isOpened() and not self.stop_record:
                    self.ret, self.frame = self.cap.read()
                    if not self.ret:
                        logging.error("Failed to grab frame from " + self.camera_name + ". Stopping recording")
                        break

                    self.out.write(self.frame)
            else:
                logging.error("No connection established with " + self.camera_name + ", record unavailable")
        except Exception as e:
            logging.error("Error while recording " + self.camera_name + ". Stopping recording.\nError: ", + e)
        finally:
            try:
                if not self.connected:
                    pass
                if self.stop_record:
                    logging.warning("Record from " + self.camera_name + " interrupted by transaction")
                logging.warning("Releasing connection of " + self.camera_name)
                self.cap.release()
                self.out.release()
                cv2.destroyAllWindows()
                logging.warning("Connection of " + self.camera_name + " released")
            except Exception as e:
                logging.error("Error while releasing " + self.camera_name + ".\nError: ", + e)
