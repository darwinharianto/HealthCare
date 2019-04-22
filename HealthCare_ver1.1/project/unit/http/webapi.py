"""
 WebAPI
 
 use exception:
     WebAPI_CommunicationFailed()
     WebAPI_RequestError()
"""
import requests
from exception import WebAPI_RequestError, WebAPI_CommunicationFailed



class WebAPI(object):
    
    
    @staticmethod
    def get(ip, port, api, data, timeout=5.0):
        try:
            url = "http://%s:%s/api/v1/%s"%(ip, port, api)
            res = requests.get(url, data=data, timeout=timeout)
        except:
            raise WebAPI_CommunicationFailed()
        
        if res.status_code != 200:
            raise WebAPI_RequestError()
    
        return res.text
    
    
    @staticmethod
    def post(ip, port, api, data, timeout=5.0):
        try:
            url = "http://%s:%s/api/v1/%s"%(ip, port, api)
            res = requests.post(url, data=data, timeout=timeout)
        except:
            raise WebAPI_CommunicationFailed()

        if res.status_code != 200:
            raise WebAPI_RequestError()
    
        return res.text
    
    
if __name__ == '__main__':
    data = WebAPI.get("52.193.188.33", 8080, "entrance", {"id":112})
    print(data)
