import RPi.GPIO as GPIO  
from time import sleep  

def gimbal_init():
    global p1,p2

    # 定义舵机引脚  
    servopin1 = 12  # 舵机1，控制方向  
    servopin2 = 13  # 舵机2，控制倾倒  

    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(servopin1, GPIO.OUT)  
    GPIO.setup(servopin2, GPIO.OUT)  

    # PWM 实例  
    p1 = GPIO.PWM(servopin1, 50)  # 舵机1的 PWM 实例  
    p2 = GPIO.PWM(servopin2, 50)  # 舵机2的 PWM 实例  

    # 启动 PWM 信号  
    p1.start(0)  # 初始占空比为0  
    p2.start(0)  # 初始占空比为0  

    # 当前角度  
    current_angle1 = 90  # 舵机1初始角度设为90，垂直状态  
    set_angle(p1, current_angle1)  # 初始化舵机1  
    set_angle(p2, 90)  # 初始化舵机2垂直位置  

def set_angle(pwm, angle):  
    if 0 <= angle <= 180:  
        pulse = 500 + (angle / 180) * (2500 - 360)  # 将角度转换为脉宽  
        duty_cycle = pulse / 10000 * 50  # 将脉宽转换为占空比  
        pwm.ChangeDutyCycle(duty_cycle)  
         # 等待舵机移动到目标位置  
    else:  
        print("角度超出范围")  



def gimbal_work(cls,current_angle1):
    if cls == 0:  # 前倾动作  
        print("向前倾")  
        set_angle(p1, current_angle1)  # 舵机1保持当前角度  
        set_angle(p2, 30)  # 舵机2向前倾倒（0°）

    elif cls == 1:  # 后倾动作  
        print("向后倾")  
        set_angle(p1, current_angle1)  # 舵机1保持当前角度  
        set_angle(p2, 150)  # 舵机2后倾（180°）

    elif cls == 2:  # 左倾动作  
        print("向左倾")  
        current_angle1 = (current_angle1 + 90)  # 舵机1向左转动90度，循环  
        set_angle(p1, current_angle1)  # 设置舵机1的新方向  
        set_angle(p2, 30)  # 舵机2向左倾倒（0°）   

    elif cls == 3:  # 右倾动作  
        print("向右倾")  
        current_angle1 = (current_angle1 - 90) # 舵机1向右转动90度，循环  
        set_angle(p1, current_angle1)  # 设置舵机1的新方向  
        set_angle(p2, 30)  # 舵机2向右倾倒（0°）  

def gimbal_reset(cls,current_angle1):
    if cls == 0:  # 前倾动作  
        print("向前倾")   
        set_angle(p2, 90)  # 返回垂直位置  
        

    elif cls == 1:  # 后倾动作  
        print("向后倾")  
        set_angle(p2, 90)  # 返回垂直位置
         

    elif cls == 2:  # 左倾动作  
        print("向左倾")   
        # current_angle1 = (current_angle1 - 90) % 360  # 重新调整当前角度 
        set_angle(p2, 90)  # 返回垂直位置  
        set_angle(p1, current_angle1)  # 舵机1不改变方向的返回姿势，也可以根据需要调整为初始角 
        

    elif cls == 3:  # 右倾动作  
        print("向右倾") 
        # current_angle1 = (current_angle1 + 90) % 360  # 重新调整当前角度  
        set_angle(p2, 90)  # 返回垂直位置
        set_angle(p1, current_angle1)  # 舵机1不改变方向的返回姿势，也可以根据需要调整为初始角 

def gimbal_deinit():
    p1.stop()  
    p2.stop()  
    GPIO.cleanup()

# try:  
#     while True:  
#         user_input = input("输入 (f: 前倾, b: 后倾, l: 左倾, r: 右倾, q: 退出): ")  

#         if user_input == "f":  # 前倾动作  
#             print("向前倾")  
#             set_angle(p1, current_angle1)  # 舵机1保持当前角度  
#             set_angle(p2, 0)  # 舵机2向前倾倒（0°）  
#             sleep(2)  # 停留2秒  
#             set_angle(p2, 90)  # 返回垂直位置  

#         elif user_input == "b":  # 后倾动作  
#             print("向后倾")  
#             set_angle(p1, current_angle1)  # 舵机1保持当前角度  
#             set_angle(p2, 180)  # 舵机2后倾（180°）  
#             sleep(2)  # 停留2秒  
#             set_angle(p2, 90)  # 返回垂直位置  

#         elif user_input == "l":  # 左倾动作  
#             print("向左倾")  
#             current_angle1 = (current_angle1 + 90) % 360  # 舵机1向左转动90度，循环  
#             set_angle(p1, current_angle1)  # 设置舵机1的新方向  
#             set_angle(p2, 0)  # 舵机2向左倾倒（0°）  
#             sleep(2)  # 停留2秒  
#             current_angle1 = (current_angle1 - 90) % 360  # 重新调整当前角度 
#             set_angle(p2, 90)  # 返回垂直位置  
#             set_angle(p1, current_angle1)  # 舵机1不改变方向的返回姿势，也可以根据需要调整为初始角  

 

#         elif user_input == "r":  # 右倾动作  
#             print("向右倾")  
#             current_angle1 = (current_angle1 - 90) % 360  # 舵机1向右转动90度，循环  
#             set_angle(p1, current_angle1)  # 设置舵机1的新方向  
#             set_angle(p2, 0)  # 舵机2向右倾倒（0°）  
#             sleep(2)  # 停留2秒  
#             current_angle1 = (current_angle1 + 90) % 360  # 重新调整当前角度  
#             set_angle(p2, 90)  # 返回垂直位置
#             set_angle(p1, current_angle1)  # 舵机1不改变方向的返回姿势，也可以根据需要调整为初始角  
  

#         elif user_input == "q":  # 按下 'q' 并退出  
#             break  

# finally:  
#     p1.stop()  
#     p2.stop()  
#     GPIO.cleanup()