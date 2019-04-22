"""
 dc320.py
 
 exception:
    SerialDeviceNotFound()

"""
import json
import serial
from common import UnitBase, IPADDR, PORT
from sdk import dc320 as SDK
from http import WebAPI
from exception import SerialDeviceNotFound

# use api
WEBAPI_USERDATA = "user_data"
WEBAPI_UPDATE   = "body_scale"



class DC320(UnitBase):


    def __init__(self):
        super(DC320, self).__init__("DC320")
        self.userInfo = None
        self.remotehost = SDK.DC320()


    def sequence(self):
        try :
            self._loadUserInfo()
#            self._setup()
#            result = self._measure()
            self._save(None)
#            self._getoff()
        except serial.serialutil.SerialException as e:
            raise SerialDeviceNotFound()
        

    def _loadUserInfo(self):
        self.userInfo = None
        data = {"ID": '%s'%self.id}
        res = WebAPI.get(IPADDR, PORT, WEBAPI_USERDATA, data)
        self.userInfo = json.loads(res)
        
    
    def _setup(self):
        self.remotehost.open()
        self.remotehost.setMode(SDK.MODE_REMOTE)
        self.remotehost.setTare(1.2)
        self.remotehost.setSex(self.userInfo["Sex"])
        self.remotehost.setBodyType(self.userInfo["BodyType"])
        self.remotehost.setAge(self.userInfo["Age"])        
    
    
    def _measure(self):
        result = self.remotehost.measureAllInOne()
        self.remotehost.buzzer(SDK.BUZZER_1)
        return result


    def _save(self, result):
        ### sample ###
#        result = '{0,16,~0,1,~1,1,~2,1,MO,"DC-320",SN,"0000000002",ID,112,DA,"19/01/30",TI,"19:59",Bt,0,GE,1,AG,56,Hm,174.0,Pt,1.5,Wk,65.6,FW,20.3,fW,13.3,MW,52.3,mW,49.6,sW,0,bW,2.7,wW,33.6,MI,22.7,Sw,63.6,OV,-5.8,IF,10,LP,106,rB,1705,rJ,10,rA,30,UF,528.3,VF,26.8,RF,471.1,XF,37.9,CS,C7'
        result = '{0,16,~0,1,~1,1,~2,1,MO,"DC-320",SN,"0000000002",ID,"%s",DA,"19/01/30",TI,"19:59",Bt,0,GE,1,AG,56,Hm,174.0,Pt,1.5,Wk,65.6,FW,20.3,fW,13.3,MW,52.3,mW,49.6,sW,0,bW,2.7,wW,33.6,MI,22.7,Sw,63.6,OV,-5.8,IF,10,LP,106,rB,1705,rJ,10,rA,30,UF,528.3,VF,26.8,RF,471.1,XF,37.9,CS,C7'%self.userInfo["ID"]
        result = self.remotehost.resultToJson(result)
        ### sample end ###
        # save database
        WebAPI.post(IPADDR, PORT, WEBAPI_UPDATE, result)
        
        
    def _getoff(self):
        self.remotehost.waitGetOff()
        

if __name__ == '__main__':
    unit = DC320()
    unit.setUserID(112)
    
    
    