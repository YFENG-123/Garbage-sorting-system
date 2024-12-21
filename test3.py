
import pigpio # 引入pigpio库  
from time import sleep # 引入计时time函数  

# 接口定义  
INT1 = 17 # 将L298 INT1口连接到树莓派Pin17  
INT2 = 18 # 将L298 INT2口连接到树莓派Pin18  
INT3 = 27 # 将L298 INT3口连接到树莓派Pin27  
INT4 = 22  # 将L298 INT4口连接到树莓派Pin22  

# 创建pigpio实例  
pi = pigpio.pi()  

# 设置引脚为输出模式  
pi.set_mode(INT1, pigpio.OUTPUT)  
pi.set_mode(INT2, pigpio.OUTPUT)  
pi.set_mode(INT3, pigpio.OUTPUT)  
pi.set_mode(INT4, pigpio.OUTPUT)  

def track_start(speed=255):  
    # 设置PWM信号  
    pi.set_PWM_dutycycle(INT1, speed)    
    pi.set_PWM_dutycycle(INT2, 0)        
    pi.set_PWM_dutycycle(INT3, speed)  
    pi.set_PWM_dutycycle(INT4, 0)      

def track_stop():  
    pi.set_PWM_dutycycle(INT1, 0)  
    pi.set_PWM_dutycycle(INT2, 0)  
    pi.set_PWM_dutycycle(INT3, 0)  
    pi.set_PWM_dutycycle(INT4, 0)  

try:  
    track_start(128)  # 启动履带，速度为128（中等速度）  
    sleep(5)          # 持续5秒  
    track_stop()      # 停止履带  

finally:  
    pi.stop()  # 关闭pigpio连接