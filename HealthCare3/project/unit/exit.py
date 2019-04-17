from base import Base as UnitBase
from base import WEBAPI_POST, WEBAPI_GET
from ..utility.json import JsonBuilder



class Exit(UnitBase):


    def __init__(self):
        super(Exit, self).__init__("exit")


    def sequence(self):
        self.updateState()


    def updateState(self):
        ### build json ###
        builder = JsonBuilder()
        builder.append("id", self.id)
        json = builder.build()
        
        ### send to api ###
        self.api(WEBAPI_POST, "exit", json)
        
        