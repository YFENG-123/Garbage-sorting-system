import pigpio
from time import sleep

# 舵机参数配置
SERVO_MIN = 500    # 0°脉宽（us）
SERVO_MAX = 2500   # 180°脉宽（us）
SERVO_MID = 1500   # 165°中点脉宽（us）

# 舵机控制引脚
SERVO1_PIN = 12  # 舵机1
SERVO2_PIN = 13  # 舵机2

def gimbal_init():
    global pi
    
    # 初始化pigpio连接
    pi = pigpio.pi()
    if not pi.connected:
        raise Exception("无法连接到pigpio守护进程，请先运行'sudo pigpiod'")
    
    # 设置初始角度
    set_angle(SERVO1_PIN, 90)
    set_angle(SERVO2_PIN, 50)  # 舵机2直立状态

def set_angle(pin, angle):
    """通用角度设置函数"""
    angle = max(0, min(180, angle))  # 限制角度范围
    pulse_width = SERVO_MIN + (angle / 180) * (SERVO_MAX - SERVO_MIN)
    pi.set_servo_pulsewidth(pin, pulse_width)

def gimbal_work(cls):

    if cls == 0:  # 前倾动作
        print("前倾")
        set_angle(SERVO2_PIN, 0)  # 舵机2向前下压
        
    elif cls == 1:  # 后倾动作
        print("后倾")
        set_angle(SERVO2_PIN, 95)  # 舵机2向后仰

    elif cls == 2:  # 左倾动作
        print("左倾")
        # 舵机1左转90度（不超过180°限制）

        set_angle(SERVO1_PIN, 175)
        set_angle(SERVO2_PIN, 0)
        
    elif cls == 3:  # 右倾动作
        print("右倾")
        # 舵机1右转90度（不低于0°限制）

        set_angle(SERVO1_PIN, 15)
        set_angle(SERVO2_PIN, 0)

def gimbal_reset():
    print("复位到中立位置")
    set_angle(SERVO2_PIN, 50)
    set_angle(SERVO1_PIN, 90)

def gimbal_deinit():
    # 停止所有舵机信号
    pi.set_servo_pulsewidth(SERVO1_PIN, 0)
    pi.set_servo_pulsewidth(SERVO2_PIN, 0)
    pi.stop()

if __name__ == "__main__":
    try:
        # 初始化云台
        gimbal_init()
        sleep(1)  # 等待1秒确保舵机初始化完成

        # 测试前倾动作
        print("测试前倾动作")
        gimbal_work(0)  # 前倾
        sleep(2)  # 等待2秒
        gimbal_reset()  # 复位
        sleep(1)  # 等待1秒

        # 测试后倾动作
        print("测试后倾动作")
        gimbal_work(1)  # 后倾
        sleep(2)  # 等待2秒
        gimbal_reset()  # 复位
        sleep(1)  # 等待1秒

        # 测试左倾动作
        print("测试左倾动作")
        gimbal_work(2)  # 左倾
        sleep(2)  # 等待2秒
        gimbal_reset()  # 复位
        sleep(1)  # 等待1秒

        # 测试右倾动作
        print("测试右倾动作")
        gimbal_work(3)  # 右倾
        sleep(2)  # 等待2秒
        gimbal_reset()  # 复位
        sleep(1)  # 等待1秒

    finally:
        # 释放资源
        print("释放资源")
        gimbal_deinit()