from abc import ABCMeta, abstractmethod

"""
 connection sever info
"""
IPADDR = "52.193.188.33"
PORT   = "8080"



"""
 common unit super class
 all unit is extend for this class. 
"""
class UnitBase(object):

    __metaclass__ = ABCMeta

    def __init__(self, name="None"):
        self._name = name
        self.id = None
        
    
    @abstractmethod
    def sequence(self, id):
        pass


    def setUserID(self, id):
        self.id = id


    def cleanup(self):
        self.id = None

