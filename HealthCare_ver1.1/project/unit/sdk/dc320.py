import serial
import re
import json

MODE_SELF   = 0
MODE_REMOTE = 1
SEX_MAN   = 0
SEX_WOMAN = 1
BODYTYPE_STANDARD = 0
BODYTYPE_ATHLETE  = 2

PRINTOUT_PATTERN1 = 0
PRINTOUT_PATTERN2 = 1
PRINTOUT_PATTERN3 = 2

LCDMODE_OFF	= 0
LCDMODE_ON	 = 1

BUZZER_1 = 1
BUZZER_2 = 2



class DC320(object):

    device = None
    FIGURE_STANDARD = None


    def __init__(self):
        # already changed static port name
        self.port = "/dev/bodyscale"
        self.bautrate 	= 9600
        self.bytesize	= 8
        self.parity		= serial.PARITY_NONE
        self.stopbits	= serial.STOPBITS_ONE
        self.timeout	= None
        self.xonxoff	= 0
        self.etscts		= 0
        self.continueTime = 0.1


    def open(self):
        # if open failed, raise for serial.serialutil.SerialException
        self.device = serial.Serial(
                self.port, self.bautrate, self.bytesize, self.parity,
                self.stopbits, self.timeout, self.xonxoff, self.etscts)
        

    def close(self):
        if not (self.device is None):
                device.close()


    def send(self, msg):
        device.write("%s\r\n"%msg)


    def recv(self):
        rcvmsg = device.readline()
        return rcvmsg


    def isError(self, recv):
        err = False
        if bool(recv == "E0"): err = True;
        if bool(recv == "E1"): err = True;
        if bool(recv == "E2"): err = True;
        if bool(recv == "E3"): err = True;
        if bool(recv == "E4"): err = True;
        if bool(recv == "E5"): err = True;
        if bool(recv == "E6"): err = True;
        if bool(recv == "E7"): err = True;
        return err


    def isBusy(self, rcvmsg):
        busy = False
        if bool(rcvmsg == "#"): busy = True;
        return busy


    def isBlank(self, rcvmsg):
        blank = False
        if bool(rcvmsg == ""): blank = True;
        return blank

    def isAtMarck(self, rcvmsg):
        atMark = False
        if bool(rcvmsg == "@"): atMark = True;
        return atMark


    #[1]
    # arg:
    #	None
    #
    # return:
    #	boolean	: function success
    def cancel(self):
        while True:
            ### send message ###
            query = "q"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            if isError(rcvmsg): return False;
            ### complete ###
            return True


    #[2]
    # arg:
    #	mode	: type integer
    #
    # return:
    #	boolean : function success
    def setMode(self, mode):
        while True:
            ### send message ###
            query = "M{}".format(mode)
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBussy(rcvmsg): sleep(self.continueTime); continue;
            if isError(rcvmsg): return False;
            ### complete ###
            return True


    #[3]
    # arg:
    #	None
    #
    # return:
    #	integer	: state number
    def getState(self):
        while True:
            ### send message ###
            query = "S?"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            return int(rcvmsg[1:2])


    #[4]
    # arg:
    #	None
    #
    # return:
    #	string[]	: parameter
    def getParameter(self):
        while True:
            ### send message ###
            query = "D?"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBussy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            result = rcvmsg.split(",")
            return result


    #[5]
    # arg:
    # 	weight  : type float
    #
    # return:
    #	boolean : function success
    def setTare(self, weight):
        ### send message ###
        query = "D0{:04.01f}".format(weight)
        self.send(query)
        ### wait receive ###
        rcvmsg = self.recv()
        ### check message ###
        if isError(rcvmsg): return False;
        ### complate ###
        return True


    #[6]
    # arg:
    #	sex		: type integer(SEX_MAN, SEX_WOMAN)
    #
    # return:
    #	boolean	: function success
    def setSex(self, sex):
        ### send message ###
        query = "D1{}".format(sex+1)
        self.send(query)
        ### wait receive ###
        rcvmsg = self.recv()
        ### check message ###
        if isError(rcvmsg): return False;
        ### complete ###
        return True


    #[7]
    # arg:
    #	type	: type integer
    #
    # return:
    #	boolean	: function success
    def setBodyType(self, type):
        ### send message ###
        query = "D2{}".format(figure)
        self.send(query)
        ### wait receive ###
        rcvmsg = self.recv()
        ### check message ###
        if isError(rcvmsg): return False;
        ### complete ###
        return True


    #[8]
    # arg:
    # 	height	: type float
    #
    # return:
    #	boolean	: function success
    def setBodyHeight(self, height):
        ### send message ###
        query = "D3{:05.01f}".format(height)
        self.send(query)
        ### wait message ###
        rcvmsg = self.recv()
        ### check message ###
        if isError(rcvmsg): return False;
        ### complete ###
        return True


    #[9]
    # arg:
    #	age		: type integer
    #
    # return:
    #	boolean	: function success
    def setAge(self, age):
        ### send message ###
        query = "D4{:02}".format(age)
        self.send(query)
        ### wait receive ###
        rcvmsg = self.recv()
        ### check message ###
        if isError(rcvmsg): return False;
        ### complete ###
        return True


    #[10]
    # arg:
    #	id		: type integer
    #
    # return:
    #	boolean	: function success
    def setID(self, id):
        ### send message ###
        query = "D5\"{:010}\"".format(id)
        self.send(query)
        ### wait receive ###
        rcvmsg = self.recv()
        ### check message ###
        if isError(rcvmsg): return False;
        ### complete ###
        return True


    #[11]
    # arg:
    #	None
    #
    # return:
    #	integer : patetrn number
    #	integer : state number
    def getPrinter_State(self):
        while True:
            ### send message ###
            query = "P?"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            pattern  = int(rcvmsg[1:2])
            state    = int(rcvmsg[3:4])
            return pattern, state


    #[12]
    # arg:
    #	None
    #
    # return:
    #	boolean	: print out success
    def printout(self):
        while True:
            ### send message ###
            query = "P1"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            if isAtMark(rcvmsg):  sleep(self.continueTime); continue;
            ### complete ###
            result = int(rcvmsg[3:4])	# 0 or 1
            return not bool(result)


    #[13]
    # arg:
    #	None
    #
    # return:
    #	integer : print pattern bumber
    def getPrinter_PrintPattern(self):
        while True:
            ### send message ###
            query = "P1"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            pattern = None
            if rcvmsg == "B000003FFFFFFC": pattern = PRINTOUT_PATTERN1
            if rcvmsg == "B000003FFFFB80": pattern = PRINTOUT_PATTERN2
            if rcvmsg == "B000003F006000": pattern = PRINTOUT_PATTERN3
            return pattern


    #[14]
    # arg:
    #	pattern	: integer(PRINTOUT_PATTERN*)
    #
    # return:
    #	boolean	: function success
    def setPrinter_PrintPattern(self, pattern):
        while True:
            ### send message ###
            query = None
            if pattern == PRINTOUT_PATTERN1: query = "B000003FFFFFFC";
            if pattern == PRINTOUT_PATTERN2: query = "B000003FFFFB80";
            if pattern == PRINTOUT_PATTERN3: query = "B000003F006000";
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            return True


    #[15]
    # arg:
    #	hh		: type integer
    #	mm		: type integer
    #	ss		: type integer
    #
    # return:
    #	boolean	: function succes
    def setTime(self, hh, mm, ss):
        while True:
            ### send message ###
            query = "T0\"{:02}:{:02}:{:02}\"".format(hh,mm,ss)
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            return True


    #[16]
    # arg:
    #	yy		: type integer
    #	mm		: type integer
    #	dd		: type integer
    #
    # return:
    # 	boolean	: function success
    def setDay(self, yy, mm, dd):
        while True:
            ### send message ###
            query = "T2\"{:02}:{:02}:{:02}\"".format(yy, mm, dd)
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            return True


    #[17]
    # arg:
    #	mode 	: integer(LCDMODE_OFF, LCDMODE_ON)
    #
    # return:
    #	boolean	: function success
    def setLCDMode(self, mode):
        while True:
            ### send message ###
            show = None
            if mode == LCDMODE_OFF: show = "D";
            if mode == LCDMODE_ON : show = "E";
            query = "F{}".format(show)
            ### wait message ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            return True


    #[18]
    # arg:
    #	None
    #
    # return;
    #	string[]	: information strings
    def getInformation(self):
        while True:
            ### send message ###
            query = "s?"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            info = rcvmsg.split(",")[1:]
            return info

    #[19]
    # arg:
    #	bzr		: integer(BUZZER_1, BUZZER_2)
    #
    # return:
    #	boolean	: function success
    def buzzer(self, bzr):
        while True:
            ### send message ###
            query = "Z{}".format(bzr)
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            return True


    #[20]
    # arg:
    #	None
    #
    # return:
    #	float	: measured value(if return None, function failed)
    def measureWeight(self):
        # send for start signal
        while True:
            ### send message ###
            query = "F0"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            if isAtMark(rcvmsg): break

        # get for process
        result = None
        while True:
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if rcvmsg[0:2] == "z0": continue;
            if rcvmsg[0:2] == "z1": continue;
            if rcvmsg[0:2] == "Wn": continue;
            if rcvmsg[0:2] == "F0": result = float(rcvmsg[6:])
            else: return None;

        # complete
        return result


    #[21]
    # arg:
    #	None
    #
    # return:
    #	float[]	: RF value, XF value
    def measureInpedance5(self):
        # send for start signal
        while True:
            ### send message ###
            query = "F5"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            if isAtMark(rcvmsg): break;

        # get for process
        while True:
            result = []
            if rcvmsg[0:1] == "I": continue;
            if rcvmsg[0:2] == "F5":
                spt = recv.split(",") # ['F5', 'RF', '????.?', 'XF', '???.?']
                rf = float(spt[2])
                xf = float(spt[4])
                result.append([rf, xf])

        # complete
        return result


    #[22]
    # arg:
    #	None
    #
    # return:
    #	float[]	: UF value, VF value 
    def measureInpedance6(self):
        # send for satrt signal
        while True:
            ### send message ###
            query = "F6"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg):
                sleep(self.continueTime)
                continue
            if isAtMark(rcvmsg):
                break

        # get for process
        while True:
            result = []
            if rcvmsg[0:1] == "I": continue;
            if rcvmsg[0:2] == "F6":
                spt = recv.split(",") # ['F6', 'UF', '????.?', 'VF', '???.?']
                uf = float(spt[2])
                vf = float(spt[4])
                result.append([uf, vf])

        # complete
        return result 


    #[23]
    # arg:
    #	None
    #
    # return:
    #	boolean	: get off
    def waitGetOff(self):
        while True:
            ### send message ###
            query = "F2"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): return False;
            if isAtMark(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            return True 


    #[24]
    # arg:
    #	None
    #
    # return:
    #	string	: measure result
    def getMeasureResult(self):
        while True:
            ### send message ###
            query = "FC"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            ### complete ###
            rcvmsg = rcvmsg[1:-1] # drop double quotation
            result = rcvmsg.split(",")
            return result


    #[25]
    # arg:
    #	None
    #
    # return:
    #	string	: measure result
    def measureAllInOne(self):
        # send for start signal
        while True:
            ### send message ###
            query = "G0"
            self.send(query)
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if isBusy(rcvmsg): sleep(self.continueTime); continue;
            if isAtMark(rcvmsg): break;

        # get for process
        while True:
            ### wait receive ###
            rcvmsg = self.recv()
            ### check message ###
            if not (rcvmsg[0:3] == "\"{0"): continue;
            ### convert to json ###
            result = rcvmsg[1:-1] # drop double quotation
            result = self.resultToJson(result)            
            return result
        

    # arg:
    #	None
    #
    # return:
    #	json	: converted result       
    def resultToJson(self, result):
        data = "{"
        result = result.split(",")
        result = json.dumps(result)
        result = json.loads(result)
        for index in range(len(result)/2):
            key = result[index*2]
            val = result[index*2+1].replace("/","")
            if key == "ID": data += '"ID":%s,'%val; continue;
            if key == "DA": data += '"Data":%s,'%val; continue;
            if key == "TI": data += '"Time":%s,'%val; continue; 
            if key == "Bt": data += '"BodyType":%s,'%val; continue;
            if key == "GE": data += '"Sex":%s,'%val; continue;
            if key == "AG": data += '"Age":%s,'%val; continue;
            if key == "Hm": data += '"BodyHeight":%s,'%val; continue;
            if key == "Pt": data += '"Tare":%s,'%val; continue;
            if key == "Wk": data += '"BodyWeight":%s,'%val; continue;
            if key == "FW": data += '"BodyFatPer":%s,'%val; continue;
            if key == "fW": data += '"BodyFatMass":%s,'%val; continue;
            if key == "MW": data += '"LeanBodyMass":%s,'%val; continue;
            if key == "mW": data += '"MuscleMass":%s,'%val; continue;
            if key == "sW": data += '"MuscleScore":%s,'%val; continue;
            if key == "bW": data += '"BoneMass":%s,'%val; continue;
            if key == "wW": data += '"WaterMass":%s,'%val; continue;
            if key == "MI": data += '"BMI":%s,'%val; continue;
            if key == "Sw": data += '"StandardWeight":%s,'%val; continue;
            if key == "OV": data += '"DoO":%s,'%val; continue;
            if key == "IF": data += '"FatLevel":%s,'%val; continue;
            if key == "LP": data += '"LegPoint":%s,'%val; continue;
            if key == "rB": data += '"BMR":%s,'%val; continue;
            if key == "rJ": data += '"BMD":%s,'%val; continue;
            if key == "rA": data += '"BodyAge":%s,'%val; continue;
            if key == "RO": data += '"LaurelIndex":%s,'%val; continue;
            
        # to json
        data = data[:-1]
        data += "}"
        data = json.loads(data)
        # convert
        if not (data["Data"] is None): data["Data"] = "\"%s\""%data["Data"];
        if not (data["Time"] is None): data["Time"] = "\"%s\""%data["Time"];                
        return data



""" sample

#[0]
# connect
#
print("connect.")
bodyscale = BodyScale()
bodyscale.open()


#[1]
# set mode (reset)
#
bodyscale.setMode(MODE_REMOTE)


#[2]
# set parameter
#
bodyscale.setTare(1.5)
bodyscale.setSex(SEX_WOMAN)
bodyscale.setFigure(FIGURE_STANDARD)
bodyscale.setHeight(175.0)
bodyscale.setAge(30)


#[3]
# measure start
#
result = bodyscale.measureAllInOne()


#[4]
# result process
#
result = resultToJSON(result)


#[5]
# complete
#
bodyscale.buzzer(BUSSER_2)


#[6]
# print out
#
if not bodyscale.printout():
	return False


#[7]
# check get off base
#
if not waitGetOff():
	return False


#[8]
# disconnect
#
bodyscale.close()
print("disconnect.")


"""
