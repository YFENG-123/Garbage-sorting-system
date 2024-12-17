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

## GPIO Pins
- GPIO模式为BCM:
  - GPIO_Compressor使用引脚23、24
  - GPIO_Gimbal使用引脚12、13
  - GPIO_Track使用引脚17、18、27、22

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
### 4.电控-GPIO

   - #### 1.GPIO_Gimbal

   使用gpiozero库的GPIO延时控制云台或者使用RPI.GPIO库写的四自由度云台控制

   -   使用gpiozero库
       - 设置校正值，将servo.value映射到一定范围调试代码，具体请看GPIO_Gimbal.py文件.
       - 抖动大，转动角度较小,响应较慢

   -   使用RPI.GPIO库
       - 封装好了up(),down(),left(),right(),方便调用.  
       - 转动角度封装在列表内，方便debug.    
       - 针对gpiozero中出现的抖动，进行了消抖操作。舵机会发生抖动是因为精度原因，它自己认为还没有达到要求的角度，所以会不断的左右纠正，最终产生抖动，所以当舵机转到指定的角度后，sleep极短时间，就将当前的占空比清零，从而进行消抖.



   - #### 2.GPIO_Track
   
     使用RPI.GPIO库写的简单正转,
     树莓派PWM IO口有限，直接使用两种转速的不同的直流电机实现两级履带差速运动

   - #### 3.GPIO_Compressor

     使用RPI.GPIO库写的简单正负极互换以及延时实现压缩
