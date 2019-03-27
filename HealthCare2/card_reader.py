# card_reader.py

import os
import nfc
import time
import binascii
import string


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
    
    def read_wait(self):
        self.connect()
        return True, self.idm
        
    
    def on_connect(self):
        self.proc = str(self.proc)
        self.idm = str(str(proc.split(":")[4:5]).replace(" ", "").split("\\n")[0][2:])
        if (not (all(c in string.hexdigits for c in idm)) || len(idm) != 24):
            raise AttributeError("Not valid ID")
        
        
    def connect(self):
        self.proc = subprocess.check_output(["nfc-poll"])
        on_connect();
