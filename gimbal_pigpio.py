import pigpio
from time import sleep

# 舵机参数配置
SERVO_MIN = 500    # 0°脉宽（us）
SERVO_MAX = 2500   # 270°脉宽（us）
SERVO_MID = 1500   # 165°中点脉宽（us）

# 舵机控制引脚
SERVO1_PIN = 12  # 舵机1
SERVO2_PIN = 13  # 舵机2

def gimbal_init():
    global pi, current_angle1
    
    # 初始化pigpio连接
    pi = pigpio.pi()
    if not pi.connected:
        raise Exception("无法连接到pigpio守护进程，请先运行'sudo pigpiod'")
    
    # 设置初始角度
    current_angle1 = 165  # 舵机1初始角度
    set_angle(SERVO1_PIN, current_angle1)
    set_angle(SERVO2_PIN, 165)  # 舵机2直立状态

def set_angle(pin, angle):
    """通用角度设置函数"""
    angle = max(0, min(270, angle))  # 限制角度范围
    pulse_width = SERVO_MIN + (angle / 270) * (SERVO_MAX - SERVO_MIN)
    pi.set_servo_pulsewidth(pin, pulse_width)

def gimbal_work(cls):
    global current_angle1

    if cls == 0:  # 前倾动作
        print("前倾")
        set_angle(SERVO2_PIN, 75)  # 舵机2向前下压
        
    elif cls == 1:  # 后倾动作
        print("后倾")
        set_angle(SERVO2_PIN, 255)  # 舵机2向后仰

    elif cls == 2:  # 左倾动作
        print("左倾")
        # 舵机1左转90度（不超过270°限制）
        new_angle = min(current_angle1 + 90, 270)
        current_angle1 = new_angle 
        set_angle(SERVO1_PIN, current_angle1)
        set_angle(SERVO2_PIN, 75)
        
    elif cls == 3:  # 右倾动作
        print("右倾")
        # 舵机1右转90度（不低于0°限制）
        new_angle = max(current_angle1 - 90, 0)
        current_angle1 = new_angle
        set_angle(SERVO1_PIN, current_angle1)
        set_angle(SERVO2_PIN, 75)

def gimbal_reset():
    print("复位到中立位置")
    set_angle(SERVO2_PIN, 165)
    set_angle(SERVO1_PIN, 165)
    global current_angle1
    current_angle1 = 165

def gimbal_deinit():
    # 停止所有舵机信号
    pi.set_servo_pulsewidth(SERVO1_PIN, 0)
    pi.set_servo_pulsewidth(SERVO2_PIN, 0)
    pi.stop()
