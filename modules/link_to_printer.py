from brother_ql import BrotherQLRaster, conversion
from brother_ql.backends.helpers import send
from PIL import Image
import logging
import time

class Task():

    def __init__(self, picname):
        logging.warning("Initializing printer")

        qr = Image.open(picname)

        PRINTER = 'usb://0x04f9:0x209b'
        LABEL_NAME = '62'
        DPI_600 = False

        logging.warning("Printing...")
        qlr = BrotherQLRaster('QL-800')
        conversion.convert(qlr, [qr], LABEL_NAME, red=True)
        send(qlr.data, PRINTER)
        logging.warning("Printed!")
