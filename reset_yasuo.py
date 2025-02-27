import pigpio
import time

class Compressor:
    def __init__(self, compress_pin, reset_pin):
        """
        初始化压缩机构
        :param compress_pin: 压缩机控制引脚
        :param reset_pin: 复位控制引脚
        """
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise Exception("无法连接到pigpio守护进程，请先运行'sudo pigpiod'")

        self.compress_pin = compress_pin
        self.reset_pin = reset_pin

        # 设置引脚模式
        self.pi.set_mode(self.compress_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.reset_pin, pigpio.OUTPUT)

        # 初始化引脚状态
        self.pi.write(self.compress_pin, 0)
        self.pi.write(self.reset_pin, 0)

    def compress(self, duration):
        """
        启动压缩机
        :param duration: 压缩持续时间（秒）
        """
        print("启动压缩...")
        self.pi.write(self.compress_pin, 1)  # 启动压缩机
        self.pi.write(self.reset_pin, 0)
        time.sleep(duration)  # 持续压缩
        self.pi.write(self.compress_pin, 0)  # 停止压缩机
        print("压缩完成")

    def reset(self, duration):
        """
        复位压缩机构
        :param duration: 复位持续时间（秒）
        """
        print("启动复位...")
        self.pi.write(self.reset_pin, 1)  # 启动复位
        self.pi.write(self.compress_pin, 0)
        time.sleep(duration)  # 持续复位
        self.pi.write(self.reset_pin, 0)  # 停止复位
        print("复位完成")

    def cleanup(self):
        """清理资源"""
        self.pi.write(self.compress_pin, 0)
        self.pi.write(self.reset_pin, 0)
        self.pi.stop()

# 示例调用
if __name__ == "__main__":
    try:
        # 初始化压缩机构
        compressor = Compressor(compress_pin=23, reset_pin=24)

        # 复位压缩机构
        compressor.reset(duration=2)  # 复位2秒

    except KeyboardInterrupt:
        print("程序终止")
    finally:
        # 清理资源
        compressor.cleanup()