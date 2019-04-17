


class JsonStringBuilder(object):
    
    
    def __init__(self):
        self.clear()

        
    def clear(self):
        self.buff = []
        
        
    def append(self, key, val):
        
        self.buff.append([key,val])
        
        
    def build(self):
        result = "{"
        for key, val in self.buff:

            ### convert ###
            if type(val) is str:
                result += "\"%s\":\"%s\""%(key,val)
            elif type(val) is int:
                result += "\"%s\":%d"%(key,val)
            elif type(val) is float:
                result += "\"%s\":%f"%(key,val)

            ### demiliter ###
            result += ","

        result = result[:-1] + "}"        
        return result
        
        
        
""" sample

builder = JsonStringBuilder()
builder.append("test1", 19283)
builder.append(123, 12.34)
builder.append("test3", "testdayo")
json = builder.build()
print(json)

"""



class JsonBuilder(object):
    
    
    def __init__(self):
        self.clear()

        
    def clear(self):
        self.buff = {}
        
        
    def append(self, key, val):
        self.buff[key] = val
        
        
    def build(self):
        return self.buff
    
    
        
""" sample

builder = JsonBuilder()
builder.append("test1", 19283)
builder.append(123, 12.34)
builder.append("test3", "testdayo")
json = builder.build()
print(json)

"""