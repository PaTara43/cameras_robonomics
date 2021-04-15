import logging
import time

from brother_ql import BrotherQLRaster, conversion
from brother_ql.backends.helpers import send
from PIL import Image


class Task:

    def __init__(self, picname):
        logging.warning("Initializing printer")

        qr = Image.open(picname)

        printer = 'usb://0x04f9:0x209b'
        label_name = '62'

        logging.warning("Printing...")
        qlr = BrotherQLRaster('QL-800')
        conversion.convert(qlr, [qr], label_name, red=True)
        send(qlr.data, printer)
        logging.warning("Printed!")
