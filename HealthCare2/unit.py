import os
import ble


class Unit(object):

    def __init__(self, name="None"):
        self.name = name


    # *** need override ***
    def action(self, id):
        print("not override.")
        pass


    def sendServer(self, api, json):
        cmd = "curl -X POST 52.193.188.33:8080/api/v1/%s -H 'Accept: application/json' -H 'Content-type: application/json' -d '%s'"%(api, json)
        print(cmd)
        ret = os.system(cmd)
        if ret == 1792:
            # server not exists
            return False

        return True


#
# Entrance
#
class Entrance(Unit):

    def __init__(self):
        super(Entrance, self).__init__("entrance")


    def action(self, id):
        json = "{\"%s\":\"%s\"}"%("id", id)
        ret = self.sendServer(self.name, json)
        return ret



#
# Exit
#
class Exit(Unit):

    def __init__(self):
        super(Exit, self).__init__("exit")


    def action(self, id):
        json = "{\"%s\":\"%s\"}"%("id", id)
        ret = self.sendServer(self.name, json)
        return ret



#
# BodyScale
#
class BodyScale(Unit):

    def __init__(self):
        super(BodyScale, self).__init__("body_scale")


    def action(self, id):
        ### get weight ###
        weight = 10

        ### send server ###
        json = "{\"%s\":\"%s\", \"%s\":\"%s\"}"%("id", id, "weight", weight)
        ret = self.sendServer(self.name, json)
        return ret


