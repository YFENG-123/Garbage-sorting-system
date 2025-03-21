import pigpio
import time

def compressor_init():
    global pi, Trig, Echo, INT5, INT6

    # 定义超声波模块的GPIO口
    Trig = 19  # 发射端
    Echo = 26  # 接收端

    # 定义压缩机控制GPIO口
    INT5 = 23  # 压缩机启动
    INT6 = 24  # 复位控制

    # 初始化pigpio连接
    pi = pigpio.pi()
    if not pi.connected:
        raise Exception("无法连接到pigpio守护进程，请先运行'sudo pigpiod'")


    # 压缩机引脚初始化
    pi.set_mode(INT5, pigpio.OUTPUT)  # 压缩机控制引脚
    pi.set_mode(INT6, pigpio.OUTPUT)  # 复位控制引脚

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise Exception("无法连接到pigpio守护进程，请先运行'sudo pigpiod'")

        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        # 设置引脚模式
        self.pi.set_mode(self.trig_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.echo_pin, pigpio.INPUT)

        # 初始化变量
        self.t1 = 0  # 记录高电平开始时间
        self.t2 = 10  # 记录高电平结束时间
        self.distance = 0  # 记录距离

        # 设置回调函数，检测Echo引脚状态变化
        self.cb = self.pi.callback(self.echo_pin, pigpio.EITHER_EDGE, self._echo_callback)

    def _echo_callback(self, gpio, level, tick):
        """Echo引脚状态变化回调函数"""
        if level == 1:  # 检测到上升沿（高电平开始）
            self.t1 = tick
        elif level == 0:  # 检测到下降沿（高电平结束）
            self.t2 = tick
            # 计算时间差并转换为距离
            pulse_width = pigpio.tickDiff(self.t1, self.t2)  # 计算高电平持续时间（us）
            # pulse_width = self.t2 - self.t1

            self.distance = (pulse_width / 1000000) * 340 * 100 / 2  # 计算距离，单位cm
            # self.distance = pulse_width * 340 * 100 / 2  # 计算距离，单位换成cm  

    def get_distance(self):
        """触发超声波测距并返回距离"""
        # 发送触发信号
        self.pi.write(self.trig_pin, 1)
        time.sleep(0.000010)  # 10us高电平
        self.pi.write(self.trig_pin, 0)

        # 等待测量完成
        time.sleep(0.0001)  # 等待100us，确保测量完成
        return self.distance

    def cleanup(self):
        """清理资源"""
        self.cb.cancel()  # 取消回调
        self.pi.stop()  # 关闭pigpio连接

    def print_time(self):
        print(f"t1,t2:{self.t1},{self.t2}")

# def get_distance():
#     # 发送触发信号
#     pi.write(Trig, 1)  # 给Trig发送高电平，发出触发信号
#     time.sleep(0.00001)  # 需要至少10us的高电平信号，触发Trig测距
#     pi.write(Trig, 0)  # 停止触发信号

#     # 等待接收高电平
#     while pi.read(Echo) == 0:
#         pass
#     t1 = time.time()  # 记录信号发出的时间

#     # 等待接收低电平
#     while pi.read(Echo) == 1:
#         pass
#     t2 = time.time()  # 记录接收到反馈信号的时间

#     # 计算距离，单位换成cm
#     distance = (t2 - t1) * 340 * 100 / 2
#     return distance

# def compress_and_reset(time_to_run):
#     print("检测到障碍物，开始压缩")
#     pi.write(INT5, 1)  # 启动压缩机
#     pi.write(INT6, 0)
#     time.sleep(time_to_run)  # 持续压缩
#     pi.write(INT5, 0)  # 停止压缩
#     pi.write(INT6, 0)
#     time.sleep(0.5)  # 等待一段时间

#     print("压缩机构复位")
#     pi.write(INT6, 1)  # 启动复位
#     pi.write(INT5, 0)
#     time.sleep(time_to_run)  # 持续复位
#     pi.write(INT6, 0)
#     pi.write(INT5, 0)
#     time.sleep(0.5)  # 等待一段时间

def start_compress():
    print("检测到障碍物，开始压缩")
    pi.write(INT5, 1)  # 启动压缩机
    pi.write(INT6, 0)

def stop_compress():
    pi.write(INT5, 0)  # 停止压缩
    pi.write(INT6, 0)

def reset_compress():
    print("压缩机构复位")
    pi.write(INT6, 1)  # 启动复位
    pi.write(INT5, 0)



def compressor_deinit():
    # 关闭所有GPIO输出
    pi.write(INT5, 0)
    pi.write(INT6, 0)
    pi.stop()

# # 示例调用
# if __name__ == "__main__":
#     try:
#         compressor_init()
#         distance = get_distance()
#         print(f"距离: {distance} cm")
#         if distance < 20:  # 如果距离小于20cm，启动压缩
#             compress_and_reset(2)  # 压缩2秒
#     finally:
#         compressor_deinit()