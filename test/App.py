'''
Created on 3 dic 2021

@author: emilio
'''

import psutil as ps
import numpy as np
from multiprocessing import Process
import time

class myApp(object):
    
    ps=None

    def doWork(self,stime):
        if(self.ps==None):
            self.ps=ps.Process()
            
        start=np.sum(self.ps.cpu_times()[0:2])
        while(np.sum(self.ps.cpu_times()[0:2])-start<stime):
            pass
    
    def start(self):
        while(True):
            time.sleep(1.0);
            self.doWork(1.0)


if __name__ == "__main__":
    app=myApp()
    proc = Process(target=app.start)
    proc.start()
    
    procu=ps.Process(pid=proc.pid)
    
    i=0
    for i in range(100):
        print(procu.cpu_percent(interval=2))
        i+=1
    
    
    proc.kill()
    proc.join()
    