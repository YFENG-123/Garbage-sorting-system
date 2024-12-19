import RPi.GPIO as GPIO  
import time  # 确保导入 time 模块  
from time import sleep  



def compressor_init():  
    global Trig,Echo,INT5,INT6,safe_dis,time_to_run

    # 定义超声波模块的GPIO口  
    Trig = 19  # 发射端  
    Echo = 26  # 接收端  

    # 定义压缩机控制GPIO口  
    INT5 = 23  # 压缩机启动  
    INT6 = 24  # 复位控制  

    safe_dis = 4  # 设置一个安全距离（单位：cm）  
    time_to_run = 2  # 压缩和复位持续的时间（秒）

    # 设置接触警告  
    GPIO.setwarnings(False)  
    # 设置引脚模式为BCM模式  
    GPIO.setmode(GPIO.BCM)  
    
    # 超声波传感器引脚初始化  
    GPIO.setup(Trig, GPIO.OUT)  # 将发射端引脚设置为输出  
    GPIO.setup(Echo, GPIO.IN)    # 将接收端引脚设置为输入  
    
    # 压缩机引脚初始化  
    GPIO.setup(INT5, GPIO.OUT)  # 压缩机控制引脚  
    GPIO.setup(INT6, GPIO.OUT)   # 复位控制引脚  

# 超声波测距函数  
def get_distance():  
    GPIO.output(Trig, GPIO.HIGH)  # 给Trig发送高电平，发出触发信号  
    time.sleep(0.00001)  # 需要至少10us的高电平信号，触发Trig测距  
    GPIO.output(Trig, GPIO.LOW)  
    
    while GPIO.input(Echo) != GPIO.HIGH:  # 等待接收高电平  
        pass  
    t1 = time.time()  # 记录信号发出的时间  
    
    while GPIO.input(Echo) == GPIO.HIGH:  # 接收端还没接收到信号变成低电平就循环等待  
        pass  
    t2 = time.time()  # 记录接收到反馈信号的时间  
    
    distance = (t2 - t1) * 340 * 100 / 2  # 计算距离，单位换成cm  
    return distance  

def compress_and_reset(time_to_run):  
    print("检测到障碍物，开始压缩")  
    GPIO.output(INT5, GPIO.HIGH)  # 启动压缩机  
    GPIO.output(INT6, GPIO.LOW)  
    sleep(time_to_run)  # 持续压缩  
    GPIO.output(INT5, GPIO.LOW)  # 停止压缩  
    GPIO.output(INT6, GPIO.LOW)  
    sleep(0.5)  # 等待一段时间  

    print("压缩机构复位")  
    GPIO.output(INT6, GPIO.HIGH)  # 启动复位  
    GPIO.output(INT5, GPIO.LOW)  
    sleep(time_to_run)  # 持续复位  
    GPIO.output(INT6, GPIO.LOW)  
    GPIO.output(INT5, GPIO.LOW)  
    sleep(0.5)  # 等待一段时间  

def compressor_work():
    barrier_dis = get_distance()  # 获取当前障碍物的距离  
    print(f"当前距离: {barrier_dis:.2f} cm")  

    # 当测得距离小于安全距离时，进行压缩  
    if barrier_dis < safe_dis:  
        compress_and_reset(time_to_run)  
    else:  
        print("垃圾桶内空间足够，无需压缩")  
      

# def main():  
#     init()  
#     safe_dis = 4  # 设置一个安全距离（单位：cm）  
#     time_to_run = 2  # 压缩和复位持续的时间（秒）  

#     try:  
#         while True:  
#             barrier_dis = get_distance()  # 获取当前障碍物的距离  
#             print(f"当前距离: {barrier_dis:.2f} cm")  

#             # 当测得距离小于安全距离时，进行压缩  
#             if barrier_dis < safe_dis:  
#                 compress_and_reset(time_to_run)  
#             else:  
#                 print("垃圾桶内空间足够，无需压缩")  
            
#             sleep(1)  # 每秒检测一次  
#     except KeyboardInterrupt:  
#         print("程序终止")  
#     finally:  
#         GPIO.cleanup()  # 清理GPIO设置  

# if __name__ == "__main__":  
#     main()