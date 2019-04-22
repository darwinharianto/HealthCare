import os
import nfc as NFC
import time
import binascii
from exception import NFC_DeviceNotFound

DOUBLETOUCH_WAITTIME = 3#sec



class Pasori(object):
    
    def __init__(self):
        self.idm = 0
        self.lastidm = 0


    def read_wait(self):
        self._connect()
        return self.lastidm


    def _on_connect(self, tag):
        self.idm = binascii.hexlify(tag.idm)


    def _connect(self):
        try:
            self.beginTime = time.time()
            while True:
                clf = NFC.ContactlessFrontend('usb')
                clf.connect(rdwr={'on-connect': self._on_connect})
                clf.close()
                if (self.idm == self.lastidm) and (time.time() - self.beginTime) < DOUBLETOUCH_WAITTIME:
                    continue
                else:
                    self.lastidm = self.idm
                    self.idm = 0
                
        except IOError as e:
            raise NFC_DeviceNotFound()



if __name__ == "__main__":
    nfc = Pasori()
    while True:
        id = nfc.read_wait()
        print(id)
