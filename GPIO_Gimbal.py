import RPi.GPIO as GPIO
from time import sleep

def tonum(num):  # 用于处理角度转换的函数
    fm = 10.0 / 180.0
    num = num * fm + 2.5
    num = int(num * 10) / 10.0
    return num

servopin1 = 12   #舵机1,方向为左右转
servopin2 = 13   #舵机2,方向为上下转

servopin1 =18 # 舵机1引脚
servopin2 =23 # 舵机2引脚
GPIO.setup(servopin1, GPIO.OUT, initial=False)  
GPIO.setup(servopin2, GPIO.OUT, initial=False)  
p1 = GPIO.PWM(servopin1,50) # 舵机1的 PWM 实例
p2 = GPIO.PWM(servopin2,50) # 舵机2的 PWM 实例# 初始化舵机位置
p1.start(7.5) #0° 对应大约7.5%  
p2.start(7.5) #0° 对应大约7.5%  
sleep(0.5) # 稳定
angles = [0,90,180] # 可用角度列表
current_angle1 =1 # 舵机1的当前角度索引（对应90°）  
current_angle2 =1 # 舵机2的当前角度索引（对应90°）  

def tonum(angle):  
    return2.5 + (angle /180) *10 # 将角度转化为适合PWM的占空比

def left(): # 舵机1左转90°  
    global current_angle1 if current_angle1 >0: # 检查是否可以左转 
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
    global current_angle1 if current_angle1 < len(angles) -1: # 检查是否可以右转 
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

    except KeyboardInterrupt:  
        print("程序终止.")  
    finally:  
        p1.stop()  
        p2.stop()  
        GPIO.cleanup()

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servopin1, GPIO.OUT, initial=False)
# GPIO.setup(servopin2, GPIO.OUT, initial=False)
# p1 = GPIO.PWM(servopin1,50) #50HZ
# p2 = GPIO.PWM(servopin2,50) #50HZ

# p1.start(tonum(85)) #初始化角度
# p2.start(tonum(40)) #初始化角度
# sleep(0.5)
# p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
# p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
# sleep(0.1)

# a = 0  #云台舵机1的执行次数
# c = 9  #云台舵机1初始化角度：90度
# b = 0  #云台舵机2的执行次数
# d = 4  #云台舵机2初始化角度：40度

# q = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
#  100, 110, 120, 130, 140, 150, 160, 170, 180]  #旋转角度列表

# def left():
#     global a, c   #引入全局变量
#     a += 1
#     if c > 2:  #判断角度是否大于20度
#         c = c-1
#         g = q[c]  #调用q列表中的第c位元素
#         print('当前角度为',g)
#         p1.ChangeDutyCycle(tonum(g))  #执行角度变化，跳转到q列表中对应第c位元素的角度
#         sleep(0.1)
#         p1.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动
#         sleep(0.01)
#     else:
#         print('\n**超出范围**\n')
#         c = 9
#         g = 85  #调用q列表中的第c位元素
#         p1.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第c位元素的角度
#         sleep(0.1)
#         p1.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动
#         sleep(0.01)
       
# def right():
#     global a, c    #引入全局变量
#     if c < 16:
#         c = c+1
#         g = q[c]  #调用q列表中的第c位元素
#         print('当前角度为',g)
#         p1.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第c位元素的角度
#         sleep(0.1)
#         p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
#         sleep(0.01)
#     else:
#         print('\n****超出范围****\n')
#         c = 9
#         g = 85  #调用q列表中的第c位元素
#         p1.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第c位元素的角度
#         sleep(0.1)
#         p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
#         sleep(0.01)

# def up():
#     global b, d    #引入全局变量
#     b += 1
#     if d > 2:
#         d = d-1
#         g = q[d]  #调用q列表中的第d位元素
#         print('当前角度为',g)
#         p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
#         sleep(0.1)
#         p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
#         sleep(0.01)
#     else:
#         print('\n**超出范围**\n')
#         d = 4
#         g = q[d]  #调用q列表中的第d位元素
#         p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
#         sleep(0.1)
#         p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
#         sleep(0.01)

# def down():
#     global b, d    #引入全局变量
#     if d < 11:
#         d = d+1
#         g = q[d]  #调用q列表中的第d位元素
#         print('当前角度为',g)
#         p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
#         sleep(0.1)
#         p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
#         sleep(0.01)
#     else:
#         print('\n****超出范围****\n')
#         d = 4
#         g = q[d]  #调用q列表中的第d位元素
#         p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
#         sleep(0.1)
#         p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
#         sleep(0.01)

# if __name__ == '__main__':
# 	while True:
# 		a = input('输入:')
# 	    if a == 'a':
# 	        left()
# 	    elif a == 'd':
# 	        right()
# 	    elif a == 'w':
# 	        up()
# 	    elif a == 's':
# 	        down()


# from gpiozero import Servo
# from time import sleep
 
# myGPIO = 14
# myCorrection = 0.5
# maxPW = (2.0 + myCorrection) / 800
# minPW = (1.0 - myCorrection) / 800

# servo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)

# def set_servo_angle(value):
#     if value ==0 :
#         servo.value = 0 # 对应0°
#     elif value == 90:
#         servo.value = 0.5 # 对应90°（之后根据舵机及实验调整具体值）
#     elif value == 180:
#         servo.value = 1.0 # 对应180°
#     elif value == -90:
#         servo.value = -0.5 # 对应-90°
#     elif value == -180:
#         servo.value = -0.9 # 对应-180°
#         sleep(1) #允许舵机有时间达到目标位置
    
    
#     # 主程序循环try:
# while True:
#     print("Turning left to90°")
#     set_servo_angle(-90)
#     sleep(1)

#     print("Resetting to0°")
#     set_servo_angle(0)
#     sleep(1)

#     print("Turning left to180°")
#     set_servo_angle(-180)
#     sleep(1)

#     print("Resetting to0°")
#     set_servo_angle(0)
#     sleep(1)


#     print("Turning right to90°")
#     set_servo_angle(90)
#     sleep(1)


#     print("Resetting to0°")
#     set_servo_angle(0)
#     sleep(1)

#     print("Turning right to180°")
#     set_servo_angle(180)
#     sleep(1)

#     print("Resetting to0°")
#     set_servo_angle(0)
#     sleep(1)


 
# servo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)
#实验防炸：servo.value-1到1，倍数不宜低于800·
# while True:
#     print("Set value range -1.0 to +0.0")
#     for value in range(0,11,1):
#         value2 = (float(value) - 10) / 10
#         servo.value = value2
#         print(value2)
#         sleep(0.1)
 
#     print("Set value range +0.0 to -0.9")
#     for value in range(11,20,1):
#         value2 = (float(value) - 10) / 10 
#         servo.value = value2
#         print(value2)
#         sleep(0.1)