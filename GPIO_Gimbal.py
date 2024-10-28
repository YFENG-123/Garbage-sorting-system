from gpiozero import Servo
from time import sleep
 
myGPIO = 14
myCorrection = 0
maxPW = (2.0 + myCorrection) / 1000
minPW = (1.0 - myCorrection) / 1000

servo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)

def set_servo_angle(value):
    if value ==0 :
    servo.value = -1 # 对应0°
    elif value == 90:
    servo.value = -0.5 # 对应90°（根据舵机及实验调整具体值）
    elif value == 180:
    servo.value =0 # 对应180°
    elif value == -90:
    servo.value =0.5 # 对应-90°（需调节具体值）
    elif value == -180:
    servo.value =0.8 # 对应-180°（需调节具体值）
    sleep(1) #允许舵机有时间达到目标位置
    
    
    # 主程序循环try:
while True:
    print("Turning left to90°")
    set_servo_angle(-90)
    sleep(1)

    print("Resetting to0°")
    set_servo_angle(0)
    sleep(1)

    print("Turning left to180°")
    set_servo_angle(-180)
    sleep(1)

    print("Resetting to0°")
    set_servo_angle(0)
    sleep(1)


    print("Turning right to90°")
    set_servo_angle(90)
    sleep(1)


    print("Resetting to0°")
    set_servo_angle(0)
    sleep(1)

    print("Turning right to180°")
    set_servo_angle(180)
    sleep(1)

    print("Resetting to0°")
    set_servo_angle(0)
    sleep(1)


 
# servo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)
 
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