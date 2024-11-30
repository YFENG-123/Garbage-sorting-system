import RPi.GPIO as GPIO  
from time import sleep  

# 定义舵机引脚  
servopin1 = 12  # 舵机1，控制方向  
servopin2 = 13  # 舵机2，控制倾倒  

# 设置 GPIO 模式  
GPIO.setmode(GPIO.BCM)  
GPIO.setup(servopin1, GPIO.OUT)  
GPIO.setup(servopin2, GPIO.OUT)  

# 定义 PWM 实例  
p1 = GPIO.PWM(servopin1, 50)  # 舵机1的 PWM 实例  
p2 = GPIO.PWM(servopin2, 50)  # 舵机2的 PWM 实例  

# 启动 PWM 信号  
p1.start(0)  # 舵机1初始占空比为0  
p2.start(0)  # 舵机2初始占空比为0  

# 舵机初始角度  
initial_angle1 = 90  # 舵机1的初始角度  
initial_angle2 = 90  # 舵机2的初始角度  

def set_angle(pwm, angle):  
    """设置舵机的角度，范围0-180度"""  
    if 0 <= angle <= 180:  
        # 将角度转换为脉宽，假设1ms对应0度，2ms对应180度  
        pulse = 1 + (angle / 180) * (2 - 1)  # 计算脉宽范围(1ms - 2ms)  
        duty_cycle = pulse / 20 * 100  # 计算占空比，转化为百分比  
        pwm.ChangeDutyCycle(duty_cycle)  
        sleep(1.5)  # 等待舵机移动到目标位置  
        print(f"舵机设置到 {angle}°")  
    else:  
        print("角度超出范围")  

def return_to_initial_positions():  
    """将所有舵机返回到初始位置"""  
    print("返回到初始位置")  
    set_angle(p1, initial_angle1)  
    set_angle(p2, initial_angle2)  
    sleep(1)  # 等待舵机返回到初始位置  

def tilt_forward():  
    """前倾动作"""  
    print("执行前倾")  
    set_angle(p1, initial_angle1)  # 舵机1保持在初始位置  
    set_angle(p2, 0)                 # 舵机2前倾  
    sleep(2)                          # 停留2秒  
    return_to_initial_positions()  

def tilt_backward():  
    """后倾动作"""  
    print("执行后倾")  
    set_angle(p1, initial_angle1)  # 舵机1保持在初始位置  
    set_angle(p2, 180)              # 舵机2后倾  
    sleep(2)                        # 停留2秒  
    return_to_initial_positions()  

def tilt_left():  
    """左倾动作"""  
    print("执行左倾")  
    set_angle(p1, 0)                # 舵机1左倾  
    set_angle(p2, initial_angle2)   # 舵机2保持在初始位置  
    sleep(2)                        # 停留2秒  
    return_to_initial_positions()  

def tilt_right():  
    """右倾动作"""  
    print("执行右倾")  
    set_angle(p1, 180)              # 舵机1右倾  
    set_angle(p2, initial_angle2)   # 舵机2保持在初始位置  
    sleep(2)                        # 停留2秒  
    return_to_initial_positions()  

try:  
    # 初始化舵机到初始位置  
    return_to_initial_positions()  

    while True:  
        user_input = input("输入 (f: 前倾, b: 后倾, l: 左倾, r: 右倾, q: 退出): ").strip()  

        if user_input == "f":  
            tilt_forward()  
        elif user_input == "b":  
            tilt_backward()  
        elif user_input == "l":  
            tilt_left()  
        elif user_input == "r":  
            tilt_right()  
        elif user_input == "q":  
            print("退出程序")  
            break  
        else:  
            print("无效输入，请重新输入。")  

finally:  
    # 清理和关闭 PWM  
    p1.stop()  
    p2.stop()  
    GPIO.cleanup()