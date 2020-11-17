import cups
import logging
import time


class Task(self):

    def __init__(self):
        logging.warning("Initializing printer")
        self.conn = cups.Connection()
        self.printers = self.conn.getPrinters()
        self.printer_name =self. printers.keys()[0]

    def send_task_to_printer(self, picname):
        logging.warning("Printing...")
        self.print_id = self.conn.printFile(self.printer_name, picname, "QR-code", {})
        # Wait until the job finishes
        while self.conn.getJobs().get(self.print_id, None):
            time.sleep(1)
        logging.warning("Printed!")
