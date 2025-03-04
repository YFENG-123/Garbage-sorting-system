# 2024 工创赛垃圾分类题

## Requirements：
- Hardware :
  - Development board : Raspberry Pi 4 Models B with 8GB RAM or Raspberry Pi 5 Models B with 8GB RAM
  - Camera : USB Camera
- Software : 
  - Operator System : Raspberry Pi OS(64-bit)
  - Virtual Environment : Miniconda3 24.7.1
  - Python : 3.11.10
  - Model: Yolov11n
- Other :
  - RealVNC Viewer(Upper PC)
  - Raspberry Pi Imager(Upper PC)
  - VSCode
  - SDCard Reader


## Deploy:

### 1. 烧录系统:
   1. TF卡使用读卡器连接上位机。在上位机中使用 Paspberry Pi Imager (安装过程不做赘述)刷写对应版本树莓派系统。(可在此步骤提前配置账户和无线网络, 稍后可以使用无线网络配置树莓派)(校园网不登录时分配的 IP 地址不合法, 无法连接, 建议使用手机热点)
   2. 系统镜像刷写完成后插入树莓派运行(为了提高首次启动成功概率, 树莓派可提前上电, 进行自检后会进入 BIOS 等待. 插入 TF 卡后将自动检测并进入操作系统. 率)
### 2. 配置操作系统：
- 进入操作系统后需要先完成三个配置后重启: 
  1. 更改系统桌面的显示服务. 默认显示服务是 Wayland 因为 OpenCV 也需要使用此服务, 会发生冲突. 需要将 Wayland 改为 X11.
  2. 升级 apt 包管理器
  3. 重启之后开启 VNC 远程桌面

- #### 方法 1 若提前配置无线网络或使用网线连接树莓派至上位机
  1. 查找树莓派 IP , 可通过以下 Windows cmd 命令发现内网 IP (其他方式不赘述)
      ```
      arp -a
      ```
      
  2. 可用以下终端命令连接树莓派. 推荐使用 Vscode 的 Remote SSH 插件连接.
     ```
     ssh <username>@<IP>
     ```
      
  3. 首先执行以下命令进入系统配置界面, 选择  `6 Advanced Options` - `A6 Wayland` - `W1 X11` 开启X11服务(重启后生效,暂时先不重启)
     ```
      sudo raspi-config
     ``` 
     
  4. 返回终端执行
     ```
     sudo apt update
     ```
     更新 apt 源再执行
     ```
     sudo apt upgrade -y
     ``` 
     升级所有包, 中途会升级 SSH 服务, 连接可能会断开, 重新连接即可. 连接后重新执行 
     ```
     sudo apt upgrade -y
     ``` 
     确保升级完成(若下载缓慢可以更换 apt 源, 换源方法不做赘述) 
  5. 升级完成后命令重启树莓派, 此时桌面服务切换为 X11 .
     ```
     sudo reboot
     ``` 
     
  6. 再次执行以下命令进入系统配置界面, 选择 `3 Interface Options` - `I3 VNC` -`Yes` 开启 VNC 服务，在上位机 RealVNC Viewer 中输入 IP 地址即可连接远程桌面
     ```
     sudo raspi-config
     ``` 
     
  7.  在桌面菜单栏中选择 `Prefrences` -> `Raspberry Pi Configuration` 在 `Localisation` 中 `Set Locate` 将 `Language` 改为 `zh(Chinese)` , `Character Set` 改为 `UTF-8` 后确认重启

   - #### 方法 2 若连接显示器和键鼠
        1. 完成操作系统初始化指引
        2. 首先执行 
            ```
            sudo raspi-config
            ``` 
            进入系统配置界面, 选择  `6 Advanced Options` - `A6 Wayland` - `W1 X11` 开启X11服务(重启后生效,暂时先不重启)
        3. 连接网络后桌面会出现更新按钮，点击更新，等待完成后点击重启.
        4. 在菜单栏中选择 `Prefrences` -> `Raspberry Pi Configuration` 在 `Interface` 中开启 `VNC` 远程桌面, 在 `Localisation` 中 `Set Locate` 将 `Language` 改为 `zh(Chinese)` , `Character Set` 改为 `UTF-8` 后确认重启

  - #### 后续编写程序使用 VSCode Remote SSH 插件编写, 测试程序在 VNC 远程桌面中进行
  - #### 若手机的 5G hz WIFI无法检测到，可以尝试更换地区为中国后重启尝试
   
### 3. 配置虚拟环境:
   1. 安装 Miniconda3:
      1. 访问 Conda 官方仓库 https://repo.anaconda.com/ 下载 Miniconda3 安装脚本文件至树莓派,注意选择 aarch64 架构版本. 可直接复制下载连接在终端中使用 `wget <URL>` 进行下载
      2. 下载后的脚本文件需要修改用户权限,使用 `sudo chmod 777 <filepath>` 修改权限, 然后在终端中输入文件路径 `./<filename>` 执行脚本. 所有配置保持默认即可, 中途需要阅读协议, 按下键或者回车读完, 然后输入 `yes` 回车同意.
   2. 创建并运行虚拟环境:
      ```Linux
      conda create -n <envname> python=3.11.10
      conda activate <envname>
      ```
   3. 安装依赖包:
      ```Linux
      pip install -r requirements.txt
      ```

### 4.电控-GPIO 模块说明

#### 1. GPIO Pins

- **GPIO 模式为 BCM**:
  - **超声模块**使用引脚 `19`、`26`
  - **GPIO_Compressor**使用引脚 `23`、`24`
  - **GPIO_Gimbal**使用引脚 `12`、`13`
  - **GPIO_Track**使用引脚 `17`、`18`、`27`、`22`

---

#### 2. GPIO_Gimbal

##### 使用 `RPI.GPIO` 库
- 封装了 `up()`、`down()`、`left()`、`right()` 函数，方便调用,具体请看GPIO_Gimbal.py文件。
- 转动角度封装在列表内，方便调试。
- **消抖处理**:
  - 针对 `gpiozero` 中出现的抖动问题，进行了消抖操作。
  - 舵机抖动的原因是精度问题，舵机认为未达到指定角度，因此会不断左右纠正，导致抖动。
  - 解决方法：当舵机转到指定角度后，`sleep` 极短时间，然后将当前占空比清零，从而消除抖动。

##### 使用 `pigpio` 库(main.py最终调用)
- 由于舵机抖动问题，参考官方文档修改为 `pigpio`，抖动问题得到解决。
- 相关文件：
  - `test_pigpio.py`

###### 舵机参数配置
```python
SERVO_MIN = 500    # 0°脉宽（us）
SERVO_MAX = 2500   # 270°脉宽（us）
SERVO_MID = 1500   # 165°中点脉宽（us）
```

###### 舵机控制引脚
```python
SERVO1_PIN = 12  # 舵机1
SERVO2_PIN = 13  # 舵机2
```

##### 主要函数
- `gimbal_init()`: 初始化舵机，设置初始角度。
- `set_angle(pin, angle)`: 通用角度设置函数，限制角度范围并设置脉宽。
- `gimbal_work(cls)`: 根据输入类别执行前倾、后倾、左倾、右倾动作。
- `gimbal_reset()`: 复位到中立位置。
- `gimbal_deinit()`: 停止所有舵机信号并释放资源。

---

#### 3. GPIO_Track
- **初赛未使用**
- 使用 `RPI.GPIO` 库实现简单正转。
- 由于树莓派 PWM IO 口有限，直接使用两种转速的直流电机实现两级履带差速运动。

---

#### 4. GPIO_Compressor

##### 使用 `pigpio` 库
- 通过 `pigpio` 库实现压缩机的控制和复位功能。
- 相关文件：
  - `pigpio_Compressor.py`

##### 引脚定义
```python
Trig = 19  # 超声波发射端
Echo = 26  # 超声波接收端
INT5 = 23  # 压缩机启动
INT6 = 24  # 复位控制
```

##### 主要函数
- `compressor_init()`: 初始化压缩机和超声波模块的 GPIO 引脚。
- `start_compress()`: 启动压缩机。
- `stop_compress()`: 停止压缩机。
- `reset_compress()`: 复位压缩机。
- `compressor_deinit()`: 关闭所有 GPIO 输出并释放资源。

##### 超声波测距模块
- 使用 `UltrasonicSensor` 类实现超声波测距功能。
- **主要方法**:
  - `get_distance()`: 触发超声波测距并返回距离（单位：cm）。
  - `cleanup()`: 清理资源，取消回调并关闭 `pigpio` 连接。


#### 注意事项
- 使用 `pigpio` 库前，请确保已安装并运行 `pigpiod` 守护进程：
  ```bash
  sudo pigpiod
  ```