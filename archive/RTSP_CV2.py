"""get a rtsp streaming with openCV"""
import cv2 as cv
import logging
import logging.config
import yaml
import _thread

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS = 5
CV_CAP_PROP_FOURCC = 6
CV_CAP_PROP_FRAME_COUNT = 7
CV_CAP_PROP_MODE = 9
CV_CAP_PROP_BRIGHTNESS = 10
CV_CAP_PROP_CONTRAST = 11
CV_CAP_PROP_SATURATION = 12
CV_CAP_PROP_HUE = 13
CV_CAP_PROP_GAIN = 14
CV_CAP_PROP_EXPOSURE = 15
CV_CAP_PROP_SHARPNESS = 20
CV_CAP_PROP_AUTO_EXPOSURE = 21
CV_CAP_PROP_GAMMA = 22
CV_CAP_PROP_TEMPERATURE = 23
CV_CAP_PROP_TRIGGER = 24
CV_CAP_PROP_TRIGGER_DELAY = 25
CV_CAP_PROP_WHITE_BALANCE_RED_V = 26
CV_CAP_PROP_ZOOM = 27
CV_CAP_PROP_FOCUS = 28
CV_CAP_PROP_GUID = 29
CV_CAP_PROP_ISO_SPEED = 30
CV_CAP_PROP_BACKLIGHT = 32
CV_CAP_PROP_PAN = 33
CV_CAP_PROP_TILT = 34
CV_CAP_PROP_ROLL = 35
CV_CAP_PROP_IRIS = 36
CV_CAP_PROP_SETTINGS = 37
CV_CAP_PROP_BITRATE = 47



def prepare_logger():
    """ Config the loggers"""
    global CONSOLE_LOGGER
    global FILE_LOGGER

    with open('log_config.yml', 'r') as config:
        try:
            configuration = yaml.safe_load(config.read())
            logging.config.dictConfig(configuration)
            CONSOLE_LOGGER = logging.getLogger('console_logger')
            FILE_LOGGER = logging.getLogger('file_logger')
        except yaml.YAMLError as exc:
            print(exc)

def get_stream():
    user = 'admin'
    password = '123456'
    ip_address = '172.16.18.110'
    port = '7070'
    stream = 'stream1'
    rtsp = "rtsp://{}:{}@{}:{}/{}".format(user, password, ip_address, port, stream)


    capture = cv.VideoCapture(rtsp)

    CONSOLE_LOGGER.info('Connection established {}:{}'.format(ip_address,port))
    print("\nRTSP URL: {}".format(rtsp))
    print("Resolution: {} x {}".format(capture.get(CV_CAP_PROP_FRAME_WIDTH), capture.get(CV_CAP_PROP_FRAME_HEIGHT)))
    print("FPS: {}".format(capture.get(CV_CAP_PROP_FPS)))
    print("codec: {}".format(capture.get(6)))
    print("Number of frames: {}".format(capture.get(CV_CAP_PROP_FRAME_COUNT)))
    print("capture Mode: {}".format(capture.get(CV_CAP_PROP_MODE)))
    print("Bitrate: {} kbits/s".format(capture.get(CV_CAP_PROP_BITRATE)))
    return capture


def main():
    """ The main function"""
    capture = get_stream()

    while capture.isOpened():

        ret, frame = capture.read()
        if ret:
            cv.imshow('capturing ', frame)           

        if cv.waitKey(1) & 0xFF == ord('q') or cv.waitKey(1) == 27:
            cv.destroyAllWindows()
            break

    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    prepare_logger()
    main()

