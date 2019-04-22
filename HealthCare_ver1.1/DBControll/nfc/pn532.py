"""
 PN532.py
    
 exception:
     NFC_InvalidID
     NFC_DeviceNotFound
"""
import subprocess32 as subprocess
import string
import re
import time
from exception import NFC_InvalidID
from exception import NFC_DeviceNotFound



class PN532(object):


    def read_wait(self):
        self.idm = None
        self._connect()
        return self.idm


    def _on_connect(self):
        self.proc = str(self.proc)
        m = re.search("ID [(].*?((\w\w  )+).*", self.proc)
        if m:
            self.idm = m.group(1).replace(" ", "")
        else:
            raise NFC_InvalidID()


    def _connect(self):
        while True:
            try :
                # read id
                self.proc = subprocess.check_output(["nfc-poll"])
            except subprocess.CalledProcessError as e:
                raise NFC_DeviceNotFound()

            # analyze message
            self._on_connect()
            break;
        


if __name__ == "__main__":
    nfc = PN532()
    id = nfc.read_wait()