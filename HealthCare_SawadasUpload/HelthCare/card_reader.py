# card_reader.py

import os
import nfc
import time
import binascii
#use pn532
import subprocess
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

class NFC_byGPIO(object):

    def read_wait(self):
        self.connect()
        return True, self.idm


    def on_connect(self):
        self.proc = str(self.proc)
        self.idm = str(str(self.proc.split(":")[4:5]).replace(" ", "").split("\\n")[0][2:])
        if (not (all(c in string.hexdigits for c in self.idm)) or len(self.idm) != 16):
            raise AttributeError("Not valid ID")


    def connect(self):
        while True:
	    try:
                self.proc = subprocess.check_output(["nfc-poll"])
	        break;
	    except:
                print("Device Not Found")
        self.on_connect()



""" sample

(ret, id) = NFC_byUSB().read_wait()

ret... success or failed
id ... id


"""
