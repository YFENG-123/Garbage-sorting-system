
import RPi.GPIO as GPIO
import argparse
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
    sleep(1)

def set_angle(pwm, angle):
    """通用角度设置函数"""
    angle = max(0, min(270, angle))  # 限制角度范围
    pulse_width = SERVO_MIN + (angle/270)*(SERVO_MAX - SERVO_MIN)
    duty_cycle = (pulse_width / 20000) * 100  # 50Hz周期20ms=20000us
    pwm.ChangeDutyCycle(duty_cycle)
    sleep(0.5)  # 确保舵机运动时间

def gimbal_work(direction):
    global current_angle1
    
    if direction == "front":
        print("前倾")
        set_angle(p2, 65)  # 舵机2向前下压
        
    elif direction == "back":
        print("后倾")
        set_angle(p2, 245)  # 舵机2向后仰
        
    elif direction == "left":
        print("左倾")
        # 舵机1左转90度（不超过270°限制）
        new_angle = min(current_angle1 + 90, 270)
        current_angle1 = new_angle 
        set_angle(p1, current_angle1)
        set_angle(p2, 65)
        
    elif direction == "right":
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


if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument("direction", 
        choices=['front', 'back', 'left', 'right', 'reset'],
        help="倾倒方向：front/back/left/right/reset")
    args = parser.parse_args()

    try:
        gimbal_init()
        if args.direction == "reset":
            gimbal_reset()
        else:
            gimbal_work(args.direction)
        sleep(2)  # 保持动作2秒
        gimbal_reset()

    finally:
        gimbal_deinit()

