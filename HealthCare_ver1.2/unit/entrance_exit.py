import requests
import json


class Entrance_Exit(object):
    
    
    def setup(self, server, port):
        self.server = server
        self.port   = port
        

    def request_exit(self, id):
        data = {"ID":"%s"%id}
        res = requests.get("http://%s:%s/api/v1/%s"%(self.server, self.port, "exit"), data, timeout=5.0)
        if (res.status_code != 200): return False
        return True
    
    
    def sequence(id):
        success = self.request_exit(id)
        return success