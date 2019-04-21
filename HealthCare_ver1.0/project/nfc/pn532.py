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
        return self.idm


    def _on_connect(self):
        self.proc = str(self.proc)
        
        m = re.search(".*(error).*", self.proc)
        if m:
            raise NFC_DeviceNotFound()
        
        m = re.search("ID [(].*?((\w\w  )+).*", self.proc)
        self.idm = m.group(1).replace(" ", "")


    def _connect(self):
        while True:
	    try:
                self.proc = subprocess.check_output(["nfc-poll"])
	        break;
	    except:
                raise NFC_DeviceNotFound()
                
        self._on_connect()
        
        
        
""" sample

nfc = PN532()
id = nfc.read_wait()
print(id)

"""
