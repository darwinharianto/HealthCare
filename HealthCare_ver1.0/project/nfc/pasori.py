import os
import nfc as NFC
import time
import binascii
from exception import NFC_DeviceNotFound



class Pasori(object):


    def read_wait(self):
        self._connect()
        return self.idm


    def _on_connect(self, tag):
        self.idm = binascii.hexlify(tag.idm)


    def _connect(self):
        try:
            clf = NFC.ContactlessFrontend('usb')
            clf._connect(rdwr={'on-connect': self.on_connect})
            clf.close()
        except IOError as e:
            raise NFC_DeviceNotFound()



if __name__ == "__main__":
    nfc = Pasori()
    id = nfc.read_wait()
    print(id)