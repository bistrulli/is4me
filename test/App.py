'''
Created on 3 dic 2021

@author: emilio
'''

import psutil as ps
import numpy as np
from multiprocessing import Process
import time
import subprocess

class myApp(object):
    
    ps=None

    def doWork(self,stime):
        if(self.ps==None):
            self.ps=ps.Process()
            
        print("stress cpu")
        start=np.sum(self.ps.cpu_times()[0:2])
        while(np.sum(self.ps.cpu_times()[0:2])-start<stime):
            pass
        
        print("stress io")
        subprocess.check_call(["stress-ng","--iomix","1",
                               "--iomix-bytes","10%","-t 10s"],stdout=None)
    
    def start(self):
        while(True):
            time.sleep(1.0);
            self.doWork(1.0)


if __name__ == "__main__":
    app=myApp()
    proc = Process(target=app.start)
    proc.start()
    
    procu=ps.Process(pid=proc.pid)
    
    cpuStart_o=np.sum(procu.cpu_times()[0:2])
    ioStart_o=np.sum(procu.io_counters()[0:2])
    i=0
    for i in range(100):
        time.sleep(2)
        cpuStart_n=np.sum(procu.cpu_times()[0:2])
        ioStart_n=np.sum(procu.io_counters()[0:2])
        
        print([(cpuStart_n-cpuStart_o)/2,(ioStart_n-ioStart_o)/2])
        
        cpuStart_n=cpuStart_o
        ioStart_n=ioStart_o
        i+=1
    
    
    proc.kill()
    proc.join()
    