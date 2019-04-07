import json

class ConfigReader(object):

    def __init__(self, location):
        self.location = location
        
    def read_config(self):
        try:
            with open(self.location) as file:
                data = json.load(file)
                mode = data["MODE"]
                print(data, mode)
                return mode
        except IOError as (errno, strerror):
            print("read error occured")
            
    def write_config(self, content):
        try:
            with open(self.location, mode="w") as file:
                file.write(content)
        except:
            print("write error occured")


""" sample
test = ConfigReader("/home/pi/HealthCare/HealthCare2/config.txt").read_config()
test = ConfigReader("/home/pi/HealthCare/HealthCare2/config.txt").write_config("Body Weight")
"""
