from pygame.time import get_ticks

class Timer():
    def __init__(self,duration,function=None):
        self.init_time = 0
        self.duration = duration
        self.function = function

    def runTimer(self,x=0,y=0):
        curr_time = get_ticks()

        if(self.init_time == 0):
            self.init_time = curr_time
        
        if((curr_time-self.init_time) >= self.duration):
            if(self.function):
                self.function(x,y)
            self.init_time = 0