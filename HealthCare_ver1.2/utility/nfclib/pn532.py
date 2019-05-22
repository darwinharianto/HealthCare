"""
 PN532.py
    
 exception:
     NFC_InvalidID
     NFC_DeviceNotFound
"""

import subprocess
import string
import re
from exception import NFC_DeviceNotFound



class PN532(object):


    def read_wait(self):
        self.idm = None
        self._connect()
        success = True if (not self.idm is None) else False        
        return success, self.idm


    def _on_connect(self):
        self.proc = str(self.proc)
        error = re.search(".*(error).*", self.proc)
        if not error:
            m = re.search("ID [(].*?((\w\w  )+).*", self.proc)
            self.idm = m.group(1).replace(" ", "")


    def _connect(self):
        while True:
            try:
                self.proc = None
                self.proc = subprocess.check_output(["nfc-poll"])
                break;
            except:
                raise NFC_DeviceNotFound()
                    
        self._on_connect()
        
        
        
if __name__ == "__main__":
    nfc = PN532()
    id = nfc.read_wait()
    print(id)
