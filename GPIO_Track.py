import RPi.GPIO as GPIO  # 引入RPi.GPIO库函数命名为GPIO
from time import sleep  # 引入计时time函数

# BOARD编号方式，基于插座引脚编号
GPIO.setmode(GPIO.BCM)  # 将GPIO编程方式设置为BOARD模式

# 接口定义
INT1 = 17                               #将L298 INT1口连接到树莓派Pin17
INT2 = 18                               #将L298 INT2口连接到树莓派Pin18
INT3 = 27  # 将L298 INT3口连接到树莓派Pin27
INT4 = 22  # 将L298 INT4口连接到树莓派Pin22

# 输出模式
GPIO.setup(INT1,GPIO.OUT)
GPIO.setup(INT2,GPIO.OUT)
GPIO.setup(INT3, GPIO.OUT)
GPIO.setup(INT4, GPIO.OUT)

GPIO.output(INT1,GPIO.HIGH)
GPIO.output(INT2,GPIO.LOW)
GPIO.output(INT3, GPIO.HIGH)
GPIO.output(INT4, GPIO.LOW)
