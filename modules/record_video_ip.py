
import cv2
import logging
import time

def Recorder(config):

    logging.warning("Started recording video")

    cap = cv2.VideoCapture('rtsp://'+config['camera1']['login']+':'+config['camera1']['password']+'@'+config['camera1']['ip']+':'+config['camera1']['port'])
    # cap = cv2.VideoCapture(0)

    width = config['video']['width']
    height = config['video']['height']
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    framerate = config['video']['framerate']
    duration = config['video']['duration']
    out = cv2.VideoWriter(config['general']['output_dir'] + 'video.avi', fourcc, framerate, (width,height))

    start_time = int(time.time())
    logging.warning('Started Recording')
    while(cap.isOpened()) and (time.time() - start_time < duration):
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
            if cv2.waitKey(33) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    logging.warning("Stopped recording video")
