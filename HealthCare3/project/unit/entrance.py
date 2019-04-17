from base import Base as UnitBase
from base import WEBAPI_POST, WEBAPI_GET
from ..utility.json import JsonBuilder



class Entrance(UnitBase):


    def __init__(self):
        super(Entrance, self).__init__("entrance")


    def sequence(self):
        self.updateState()


    def updateState(self):
        ### build json ###
        builder = JsonBuilder()
        builder.append("id", self.id)
        json = builder.build()
        
        ### send to api ###
        self.api(WEBAPI_POST, "entrance", json)

        
        