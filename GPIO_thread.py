import threading
import time
import gpiozero

class GPIOThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print("启动GPIO...")
        self.gpio18 = gpiozero.LED(18)
        print("GPIO启动成功")
        self._IsRunning =True
    
    def run(self):
        while True:
            if self._IsRunning:
                self.gpio18.on()
                time.sleep(1)
                self.gpio18.off()
                time.sleep(1) 
            else:
                break
    def stop(self):
        self._IsRunning = False
