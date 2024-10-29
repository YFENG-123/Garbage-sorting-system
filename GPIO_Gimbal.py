import RPi.GPIO as GPIO
from time import sleep

def tonum(num):  # 用于处理角度转换的函数
    fm = 10.0 / 180.0
    num = num * fm + 2.5
    num = int(num * 10) / 10.0
    return num

servopin1 = 12   #舵机1,方向为左右转
servopin2 = 13   #舵机2,方向为上下转

GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin1, GPIO.OUT, initial=False)  
GPIO.setup(servopin2, GPIO.OUT, initial=False)  
p1 = GPIO.PWM(servopin1,50) # 舵机1的 PWM 实例
p2 = GPIO.PWM(servopin2,50) # 舵机2的 PWM 实例# 初始化舵机位置
p1.start(7.5) #0° 对应大约7.5%  
p2.start(7.5) #0° 对应大约7.5%  

sleep(0.5) # 稳定
angles = [0,90,180] # 可用角度列表
current_angle1 =1
current_angle2 =1

def tonum(angle):  
    return 2.5 + (angle /180) *10 # 将角度转化为适合PWM的占空比

def left(): # 舵机1左转90°  
    global current_angle1 
    if current_angle1 >0: # 检查是否可以左转 
        current_angle1 -=1 
        g = angles[current_angle1]  
        print('舵机1当前角度为', g)  
        p1.ChangeDutyCycle(tonum(g))  
        sleep(0.1)  
        p1.ChangeDutyCycle(0)  
        sleep(0.01)  
    else:  
        print('\n**舵机1已经到最左边**\n')  

def right(): # 舵机1右转90°  
    global current_angle1 
    if current_angle1 < len(angles) -1: # 检查是否可以右转 
        current_angle1 +=1 
        g = angles[current_angle1]  
        print('舵机1当前角度为', g)  
        p1.ChangeDutyCycle(tonum(g))  
        sleep(0.1)  
        p1.ChangeDutyCycle(0)  
        sleep(0.01)  
    else:  
        print('\n**舵机1已经到最右边**\n')  

def up(): # 舵机2上升90°  
    global current_angle2 
    if current_angle2 < len(angles) -1: # 检查是否可以上升 
        current_angle2 +=1 
        g = angles[current_angle2]  
        print('舵机2当前角度为', g)  
        p2.ChangeDutyCycle(tonum(g))  
        sleep(0.1)  
        p2.ChangeDutyCycle(0)  
        sleep(0.01)  
    else:  
        print('\n**舵机2已经到最上面**\n')  

def down(): # 舵机2下降90°  
    global current_angle2 
    if current_angle2 >0: # 检查是否可以下降 
        current_angle2 -=1
        g = angles[current_angle2]  
        print('舵机2当前角度为', g)  
        p2.ChangeDutyCycle(tonum(g))  
        sleep(0.1)  
        p2.ChangeDutyCycle(0)  
        sleep(0.01)  
    else:  
        print('\n**舵机2已经到最底部**\n')  

#if __name__ == '__main__':  
#try:  
while True:  
    a = input('输入 (a: 左转, d:右转, w: 上升, s:下降): ')  
    if a == 'a':  
        left()  
    elif a == 'd':  
        right()  
    elif a == 'w':  
        up()  
    elif a == 's':  
        down()  

