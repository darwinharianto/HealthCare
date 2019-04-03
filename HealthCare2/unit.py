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
# Application
#
class Apply(Unit):

    def __init__(self):
        super(Apply, self).__init__("apply")


    def action(self, id):
        json = "{\"%s\":\"%s\", \"%s\":\"%s\", \"%s\":%s}"%("id", id, "name", "sawada", "io", 0)
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
        central = ble.Central()
        while True:
            devs = central.scan("00000000-0000-0000-0000-000000000002")
            if not devs == None:
                break
        central.connectTo(devs[0])
        handle = central.getHandle("00000000-0000-0000-0000-000000000002")
        print("read", handle)
        data = central.readCharacteristic(handle)
        message = "found you"
        central.writeCharacteristic(handle, bytes(message))
        if data is None:
            print("None")
        else:
            print(data)
        central.disconnect()
        ### send server ###
        json = "{\"%s\":\"%s\", \"%s\":\"%s\"}"%("id", id, "weight", data)
        ret = self.sendServer(self.name, json)
        return ret


