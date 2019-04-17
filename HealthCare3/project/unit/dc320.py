from base import Base as UnitBase
from base import WEBAPI_POST, WEBAPI_GET
from ..utility.json import JsonBuilder
from ..sdk.dc320 import DC320 as SDK



class DC320(UnitBase):


    def __init__(self):
        super(DC320, self).__init__("DC320")


    def sequence(self):
        ### get parameter from database ###
        param = self.getParamFromDataBase()
        ### set parameter to dc320
        self.setParamToUnit(param)
        
        
    def getParamFromDataBase(self):
        ### build json ###
        builder = JsonBuilder()
        builder.append("id", self.id)
        json = builder.build()
        
        ### send to api ###
        res = self.api(WEBAPI_GET, "user_data", json)
        # TODO
        # return value is string
        # convert to json
        return res
        
        
    def setParamToUnit(self, json):
        SDK.setAge(param["Age"])
        # TODO 
        pass
    
                 