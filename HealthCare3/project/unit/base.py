import requests
from abc import ABCMeta, abstractmethod


IPADDR = "52.193.188.33"
PORT   = "8080"

WEBAPI_POST = 0
WEBAPI_GET  = 1



class Base(object):

    __metaclass__ = ABCMeta

    def __init__(self, name="None"):
        self._name = name
        self._ip   = IPADDR
        self._port = PORT
        self.id = None
        
    
    @abstractmethod
    def sequence(self, id):
        pass


    def setUserID(self, id):
        self.id = id


    def cleanup(self):
        self.id = None


    def api(self, x, api, dict):
        ### execute type ###
        res = None
        if x == WEBAPI_GET : res = self._getAPI(api, dict)        
        if x == WEBAPI_POST: res = self._postAPI(api,dict)

        ### check response ###
        if res.status_code != 200:
            raise WebAPI_RequestError()
        
        print(res.text)
        return res.text
        
    
    def _getAPI(self, api, dict):
        res = requests.get("http://%s:%s/api/v1/%s"%(IPADDR, PORT, api), json=dict, timeout=1.0)
        return res


    def _postAPI(self, api, dict):
        res = requests.post("http://%s:%s/api/v1/%s"%(IPADDR, PORT, api), json=dict, timeout=1.0)
        return res
        
    
            