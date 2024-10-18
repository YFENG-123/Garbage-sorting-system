# 2024 工创赛垃圾分类题

## Requirements：
- Hardware :
  - Development board : Raspberry Pi 4 Models B with 8GB RAM
  - Camera : USB Camera
- Software : 
  - Operator System : Raspberry Pi OS(64-bit)
  - Virtual Environment : Miniconda3 24.7.1
  - Python : 3.11.10
    - Packages :
      - opencv-python : 4.10.0.84
      - pillow : 11.0.0
      - gpiozero : 2.0.1
      - rpi.gpio : 0.7.1
      - pigpio :1.78
      - lgpio : 0.2.2.0
- Other :
  - RealVNC Viewer(Upper PC)
  - Raspberry Pi Imager(Upper PC)
  - VSCode
  - SDCard Reader

## GPIO Pins

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
  