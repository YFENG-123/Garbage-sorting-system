import cv2
import time
import os
import random
from PIL import Image
from gimbal_pigpio_v3 import gimbal_init, gimbal_work, gimbal_reset, gimbal_deinit

from datetime import datetime  # 导入 datetime 模块

# 初始化舵机
gimbal_init()
gimbal_reset()

# 设置图像保存路径
save_folder = "captured_images"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 设置拍摄频率（秒）
capture_interval = 0.2 

# 设置舵机运动的随机时间范围（秒）
min_random_time = 0.3  # 最小随机时间
max_random_time = 0.6  # 最大随机时间


# 舵机运动方向控制
gimbal_status = 0

# 初始化摄像头
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    camera = cv2.VideoCapture(1)

# 设置摄像头分辨率（可选）
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

def capture_and_save_image():
    ret, frame = camera.read()
    if not ret:
        print("Failed to capture image")
        return

    # 裁剪图像为正方形
    height, width = frame.shape[:2]
    min_dim = min(height, width)
    start_x = (width - min_dim) // 2
    start_y = (height - min_dim) // 2
    cropped_frame = frame[start_y:start_y + min_dim, start_x:start_x + min_dim]

    # 保存图像
    # 获取当前时间，精确到毫秒
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # %f 是微秒，取前3位表示毫秒
    image_path = os.path.join(save_folder, f"{timestamp}.jpg")
    cv2.imwrite(image_path, cropped_frame)
    print(f"Image saved: {image_path}")

def control_gimbal():

    global gimbal_status
    gimbal_status = (gimbal_status + 1)%8
    print("下一运动模式：",gimbal_status)
    if gimbal_status & 1 == 1:
        gimbal_reset()
    else:
        # 控制舵机运动
        gimbal_work(int(gimbal_status/2))  # 假设舵机运动模式为1

    print("Gimbal movement completed")

try:
    last_gimbal_time = time.time()  # 记录上次舵机运动的时间
    next_gimbal_time = round(random.uniform(min_random_time, max_random_time), 2)  # 生成下次舵机运动的随机时间

    while True:
        current_time = time.time()

        # 捕获并保存图像
        capture_and_save_image()

        # 检查是否到达随机时间，控制舵机运动
        if current_time - last_gimbal_time >= next_gimbal_time:
            control_gimbal()
            last_gimbal_time = current_time  # 更新上次舵机运动的时间
            next_gimbal_time = round(random.uniform(min_random_time, max_random_time), 2)  # 生成新的随机时间
            print(f"Next gimbal movement in {next_gimbal_time} seconds")

        # 等待拍摄间隔
        time.sleep(capture_interval)

except KeyboardInterrupt:
    print("Program terminated")

finally:
    # 释放资源
    camera.release()
    gimbal_deinit()