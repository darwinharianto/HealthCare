import json
from common import UnitBase, IPADDR, PORT
from http import WebAPI
"""
use api
"""
WEBAPI_EXIT = "exit"



class Exit(UnitBase):


    def __init__(self):
        super(Exit, self).__init__("exit")


    def sequence(self):
        self._sendToServer()


    def _sendToServer(self):
        data = {"ID": '%s'%self.id}
        WebAPI.post(IPADDR, PORT, WEBAPI_EXIT, data)
        
    
    
if __name__ == '__main__':
    unit = Exit()
    unit.setUserID(112)
    unit.sequence()