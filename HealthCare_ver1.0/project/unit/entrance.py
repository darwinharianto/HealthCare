import json
from common import UnitBase, IPADDR, PORT
from http import WebAPI

# use api
WEBAPI_ENTRANCE = "entrance"



class Entrance(UnitBase):


    def __init__(self):
        super(Entrance, self).__init__("entrance")


    def sequence(self):
        self._sendToServer()


    def _sendToServer(self):
        data = {"ID": '%s'%self.id}
        WebAPI.post(IPADDR, PORT, WEBAPI_ENTRANCE, data)
        
        
    
if __name__ == '__main__':
    unit = Entrance()
    unit.setUserID(112)
    unit.sequence()