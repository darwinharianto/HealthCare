import time



class Timer(object):
    
    
    def __init__(self, time):
        self.time = time
        self.lastTime = None
        pass
    
    
    def start(self):
        if self.lastTime is None:   
            self.lastTime = time.time()
        
    
    def is_over(self):
        return True if (time.time() - self.lastTime) > self.time else False
            
        
    def reset(self):
        self.lastTime = None


    def is_enable(self):
        return False if (self.lastTime is None) else True



if __name__ == "__main__":
    timer = Timer(5)
    if not timer.is_enable():
        timer.start()
    
    while timer.is_enable():
        if timer.is_over():
            print("time over.")
            timer.reset()
        else:
            print("time on.")
            time.sleep(0.5)
