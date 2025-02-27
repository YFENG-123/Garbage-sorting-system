import RPi.GPIO as GPIO
from time import sleep

# 舵机参数配置
SERVO_MIN = 500    # 0°脉宽（us）
SERVO_MAX = 2500   # 270°脉宽（us）
SERVO_MID = 1500   # 135°中点脉宽（us）

def gimbal_init():
    global p1, p2, current_angle1
    
    # GPIO初始化
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)  # 舵机1
    GPIO.setup(13, GPIO.OUT)  # 舵机2

    # PWM初始化
    p1 = GPIO.PWM(12, 50)
    p2 = GPIO.PWM(13, 50)
    p1.start(0)
    p2.start(0)

    # 初始角度（对应中点）
    current_angle1 = 155 # 舵机1初始角度
    set_angle(p1, current_angle1)
    set_angle(p2, 155)    # 舵机2直立状态

def set_angle(pwm, angle):
    """通用角度设置函数"""
    angle = max(0, min(270, angle))  # 限制角度范围
    pulse_width = SERVO_MIN + (angle/270)*(SERVO_MAX - SERVO_MIN)
    duty_cycle = (pulse_width / 20000) * 100  # 50Hz周期20ms=20000us
    pwm.ChangeDutyCycle(duty_cycle)
    sleep(0.5)  # 确保舵机运动时间



def gimbal_work(cls):
    global current_angle1

    if cls == 0:  # 前倾动作  
        print("前倾")
        set_angle(p2, 65)  # 舵机2向前下压
        
    elif cls == 1:  # 后倾动作  
        print("后倾")
        set_angle(p2, 245)  # 舵机2向后仰

    elif cls == 2:  # 左倾动作  
        print("左倾")
        # 舵机1左转90度（不超过270°限制）
        new_angle = min(current_angle1 + 90, 270)
        current_angle1 = new_angle 
        set_angle(p1, current_angle1)
        set_angle(p2, 65)
        
    elif cls == 3:  # 右倾动作  
        print("右倾")
        # 舵机1右转90度（不低于0°限制）
        new_angle = max(current_angle1 - 90, 0)
        current_angle1 = new_angle
        set_angle(p1, current_angle1)
        set_angle(p2, 65) 

def gimbal_reset():
    print("复位到中立位置")
    set_angle(p2, 155)
    set_angle(p1, 155)



def gimbal_deinit():
    p1.stop()
    p2.stop()
    GPIO.cleanup()

