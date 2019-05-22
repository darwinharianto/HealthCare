import requests
import json
from sdk import dc320 as sdk



class DC320(object):


    def setup(self, server, port):
        self.server = server
        self.port   = port


    def request_userinfo(self, id):
        data = {"ID":"%s"%id}
        res = requests.get("http://%s:%s/api/v1/%s"%(self.server, self.port, "user_data"), data, timeout=5.0)
        if (res.status_code != 200): return False, None
        userinfo = json.loads(res.text) if not (res.text == "") else None
        return True, userinfo


    def request_update(self, id, result):
        result = sdk.result_to_dict(result)
        result["ID"] = id
        res = requests.post("http://%s:%s/api/v1/%s"%(self.server, self.port, "body_scale"), result, timeout=5.0)
        if (res.status_code != 200): return False
        return True
        

    def sequence(self, id):
        # get user info
        success, userinfo = self.request_userinfo(id)
        if (not success) or (userinfo is None):
            return False   
            
        # measure
        success, result = self.measure(userinfo)
        if not success:
            return False
        
        # update
        if not self.request_update(id, result):
            return False
        
        return True
        
        
    def measure(self, userinfo):
        abort = False
        result = ""

        sdk.sequence("open device.")
        dev = sdk.openDevice("/dev/ttyUSB0")
        
        if not abort:
            sdk.sequence("set mode.");
            if not sdk.setMode(dev, 1):
                abort = True
        
        if not abort:
            sdk.sequence("set tare.")
            if not sdk.setTare(dev, 1.5):
                abort = True
        
        if not abort:
            sdk.sequence("set sex.")
            if not sdk.setSex(dev, userinfo["Sex"]):
                abort = True

        if not abort:
            sdk.sequence("set body type.")
            if not sdk.setBodyType(dev, userinfo["BodyType"]):
                abort = True
        
        if not abort:
            sdk.sequence("set body height.")
            if not sdk.setBodyHeight(dev, 173.4):
                abort = True
        
        if not abort:
            sdk.sequence("set age.")
            if not sdk.setAge(dev, 29):
                abort = True
        
        if not abort:
            sdk.sequence("start measure.")
            if not sdk.startMeasure(dev):
                abort = True

        if not abort:
            sdk.sequence("wait result.")
            success, result = sdk.waitResult(dev)
            if (not success):
                abort = True
        
        if not abort:
            sdk.sequence("measure end.")
            if not sdk.buzzer1(dev):
                abort = True
        
        if not abort:
            sdk.sequence("wait getoff.")
            if not sdk.waitGetoff(dev):
                abort = True

        sdk.sequence("clear")
        sdk.setMode(dev, 1)
        dev.close()

        if abort:
            return False, None

        return True, result
            
            
            
if __name__ in "__main__":
    
    unit = DC320()
    if not unit.sequence("112"):
        print("abort!")
    else:
        print("complete!")
    