import project.unit as unit

#unit = unit.DC320()
#unit.setUserID("112")
#res = unit.getParamFromDataBase()

#unit = unit.Exit()
#unit.setUserID("112")
#res = unit.sequence()

unit = unit.Entrance()
unit.setUserID("112")
res = unit.sequence()
print(res)