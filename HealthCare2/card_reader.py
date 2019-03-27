# card_reader.py

import os
import nfc
import time
import binascii


# ----------------------------------------------------------------------- #
# util class
class NFC_byUSB(object):

    def read_wait(self):
        self.connect()
        return True, self.idm


    def on_connect(self, tag):
        self.idm = binascii.hexlify(tag.idm)


    def connect(self):
        self.result = False
        try:
            clf = nfc.ContactlessFrontend('usb')
            clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            clf.close()

# ----------------------------------------------------------------------- #

class CardReader_GPIO:
    def empty(self):
        return None
