import RPi.GPIO as GPIO  
from time import sleep   

# 设置GPIO模式  
GPIO.setmode(GPIO.BCM)  

# 定义引脚  
INT5 = 23  # L298 INT1口连接到树莓派Pin23（正转）  
INT6 = 24  # L298 INT2口连接到树莓派Pin24（反转）  

# 设置引脚为输出  
GPIO.setup(INT5, GPIO.OUT)  
GPIO.setup(INT6, GPIO.OUT)  

# 定义运动参数  
distance_to_push = 100  # 推送100mm 
speed = 50  # 转速50mm/s  
time_to_run = distance_to_push / speed  # 时间 = 距离 / 速度  

try:    
    while True:  
        user_input = input("输入 (w:压缩, s:复位, q:退出): ")  
        # 检测键盘输入  
        if user_input == "w":  # 按下 'w',压缩
            print("推送前进 10 cm")  
            GPIO.output(INT5, GPIO.HIGH) 
            GPIO.output(INT6, GPIO.LOW)   
            sleep(time_to_run)  
            GPIO.output(INT5, GPIO.LOW)  
            GPIO.output(INT6, GPIO.LOW)  
            sleep(0.5) 

        elif user_input == "s":  # 按下 'w',复位
            print("后退 10 cm")  
            GPIO.output(INT6, GPIO.HIGH) 
            GPIO.output(INT5, GPIO.LOW)    
            sleep(time_to_run)  
            GPIO.output(INT6, GPIO.LOW)  
            GPIO.output(INT5, GPIO.LOW)   
            sleep(0.5)   

        elif user_input == "q":  # 按下 'q' 并退出  
            print("退出程序")  
            break  

finally:  
    # 清理GPIO设置  
    GPIO.cleanup()

#定义引脚
#GPIO_OUT = 23
#GPIO_OUT = 24
#led = 21

#设置23针脚为输入，接到红外避障传感器模块的out引脚

# GPIO.setup(GPIO_OUT,GPIO.IN)

# GPIO.setup(led,GPIO.OUT)

# def warn(): #亮灯来作为有障碍物时发出的警告

#     GPIO.output(led,GPIO.HIGH)

#     time.sleep(0.5)

#     GPIO.output(led,GPIO.LOW)

#     time.sleep(0.5)

# while True:
#     if GPIO.input(GPIO_OUT)==0: #当有障碍物时，传感器输出低电平，所以检测低电平
#         warn()
#         #print("There has a barrier")
#     #else:
#        # print("OK")

# GPIO.cleanup()
