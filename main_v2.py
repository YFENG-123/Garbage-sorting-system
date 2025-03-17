
#import gpiozero
import time
from datetime import datetime
import cv2 
import ttkbootstrap as ttk

from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from ultralytics import YOLO
from PIL import Image, ImageTk  # 图像控件
Image.CUBIC = Image.BICUBIC # 显式修复ttk包bug

from gimbal_pigpio_v2 import gimbal_init,gimbal_work,gimbal_reset,gimbal_deinit
from GPIO_Track import track_init,track_start,track_stop
from pigpio_Compressor import compressor_init,start_compress,stop_compress,reset_compress,UltrasonicSensor

import pi_system
from count_time import get_elapsed_time
from meanfilter import MeanFilter


class GUI:
    
    # 模式
    mode = 0

    # 模式切换时间
    mode_transfrom_time = 30

    # 视频播放速度
    speed = 4.0

    # 模式持续时间
    mode_t1 = 0

    # 模型标志
    model_flag = 0

    # 系统工作状态
    system_status = 0

    # 垃圾识别判断
    waste_exist_frame = 0 # 垃圾识别帧
    waste_exist_frame_max = 5 # 垃圾识别帧阈值
    waste_exist_flag = True # 垃圾识别结果
    waste_total = 0 # 垃圾总数
    mean_conf = 0 # 平均概率
    conf_threshold = 0.75 # 平均置信率

    # 舵机运行方向
    duoji_start_time = 0

    # 压缩机构
    compressor_work_status = 0 # 压缩机构工作状态
    safe_dis = 5.0  # 设置一个安全距离（单位：cm）  
    time_to_run = 7  # 压缩和复位持续的时间（秒）
    compressor_t1 = 0 # 压缩开始时间
    window_size = 5 # 均值滤波窗口大小

    #摄像头图片参数
    image_multiple = 50
    image_width = 16*image_multiple
    image_height = 9*image_multiple

    #静态图片防止闪烁
    static_image_container = None
    
    #帧时间戳
    num_frames = 70
    frames_count = 0
    time_stamp = 0.0
    last_time_stamp = 0.0
    FPS = 0

    # 初始化
    def __init__(self):

        #载入模型
        
        print("载入模型...")

        self.cls_ncnn_model = YOLO("model/wasteCls_v4_ncnn_model",task='classify')

        # self.det_ncnn_model = YOLO("model/yolo11n_det_320_ncnn_model",task='detect')
        print("模型载入完毕")

    # ... (其余初始化代码保持不变)

        #启动摄像头（较费时），载入视频
        print("启动摄像头...")
        self.camera = cv2.VideoCapture(0) # cv初始化摄像头 
        if not self.camera.isOpened(): 
            self.camera = cv2.VideoCapture(1)
        self.video = cv2.VideoCapture("Video_v2.mp4")# cv初始化视频
        print("摄像头启动成功")

        #初始化GPIO
        print("初始化GPIO...")
        gimbal_init()
        track_init()
        self.meanFilter = MeanFilter(self.window_size)
        compressor_init()
        self.ultrasonic = UltrasonicSensor(trig_pin=19, echo_pin=26)
        track_start()
        print("GPIO启动成功")
        
        # 创建窗口
        self.root = ttk.Window()
        
        # 设置风格字体
        style = ttk.Style("solar")
        style.configure('TLabelframe.Label', font=("Arial",12))
        style.configure('custom.primary.Treeview.Heading', font=('Arial', 15))  # 设置表头字体
        style.configure('custom.primary.Treeview',rowheight=30, font=('Arial', 10))

        # 各类属性
        self.tableview_items_num = 12
        self.progressbar_length = 335
        self.tableview_column_width = 115
        self.metersize = 190
        self.waste_logo_size = 30

        # 读取各类垃圾图标
        self.image_food_waste = ImageTk.PhotoImage(Image.open("gui_images/food_waste_logo.png").resize((self.waste_logo_size,self.waste_logo_size)))
        self.image_recyclable_waste = ImageTk.PhotoImage(Image.open("gui_images/recyclable_waste_logo.png").resize((self.waste_logo_size,self.waste_logo_size)))
        self.image_other_waste = ImageTk.PhotoImage(Image.open("gui_images/other_waste_logo.png").resize((self.waste_logo_size,self.waste_logo_size)))
        self.image_hazardous_waste = ImageTk.PhotoImage(Image.open("gui_images/hazardous_waste_logo.png").resize((self.waste_logo_size,self.waste_logo_size)))
        self.wastes_cls = ['None','Food Waste','Hazardous Waste','Other Waste','Recyclable Waste']
        self.waste_count = [0,0,0,0]

        # 界面编写
        self.interface()

        # 启动更新函数
        self.update_frame() 
    # 界面编写
    def interface(self):
        self.create_history_frame()
        self.create_total_frame()
        self.create_video_frame()
        self.create_status_frame()
        self.create_system_frame()
    
    # 历史记录框
    def create_history_frame(self):

        # 标签框
        self.labelframe_history = ttk.Labelframe(self.root, text="History")
        self.labelframe_history.grid(row=0, column=0,rowspan=1,padx=1,pady=1,ipadx=2,ipady=2)

        # 列表框
        colors = self.root.style.colors

        coldata = [
            {"text": "Order", "stretch": False,"width": self.tableview_column_width},
            {"text": "Class", "stretch": False,"width": self.tableview_column_width},
            {"text": "Num", "stretch": False,"width": self.tableview_column_width},
            {"text": "Status", "stretch": False,"width": self.tableview_column_width}
            
        ]

        rowdata = [

        ]
        self.tableview_history = Tableview(
            master=self.labelframe_history,
            coldata=coldata,
            rowdata=rowdata,
            paginated=False,
            searchable=False,
            bootstyle=INFO,
            stripecolor=(colors.success, None),
            height=self.tableview_items_num,
            pagesize=self.tableview_items_num,
        )
        self.tableview_history.grid()
        self.tableview_history.configure(style='custom.primary.Treeview')  # 应用自定义样式
    
    # 投放统计框
    def create_total_frame(self):
        
        # 标签框
        self.labelframe_total = ttk.Labelframe(self.root, text="Garbage Disposal Statistics")
        self.labelframe_total.grid(row=0, column=2,rowspan=1,padx=1,pady=1,ipadx=2,ipady=2,sticky='news')

        # 各类垃圾标签框
        self.labelframe_food_waste = ttk.Labelframe(self.labelframe_total,text='Food Waste',bootstyle="success")
        self.labelframe_food_waste.grid(row=0,column=0,padx=5,pady=5,ipadx=2,ipady=2)
        self.labelframe_recyclable_waste = ttk.Labelframe(self.labelframe_total,text='Recyclable Waste',bootstyle="primary")
        self.labelframe_recyclable_waste.grid(row=1,column=0,padx=5,pady=5,ipadx=2,ipady=2)
        self.labelframe_other_waste = ttk.Labelframe(self.labelframe_total,text='Other Waste',bootstyle="secondary")
        self.labelframe_other_waste.grid(row=2,column=0,padx=5,pady=5,ipadx=2,ipady=2)
        self.labelframe_hazardous_waste = ttk.Labelframe(self.labelframe_total,text='Hazardous Waste',bootstyle="danger")
        self.labelframe_hazardous_waste.grid(row=3,column=0,padx=5,pady=5,ipadx=2,ipady=2)

        # 各类垃圾图标
        self.label_food_waste = ttk.Label(self.labelframe_food_waste,text="Food Waste",image=self.image_food_waste)
        self.label_food_waste.grid(row=0,column=0)
        self.label_recyclable_waste = ttk.Label(self.labelframe_recyclable_waste,image=self.image_recyclable_waste)
        self.label_recyclable_waste.grid(row=0,column=0)
        self.label_other_waste = ttk.Label(self.labelframe_other_waste,image=self.image_other_waste)
        self.label_other_waste.grid(row=0,column=0)
        self.label_hazardous_waste = ttk.Label(self.labelframe_hazardous_waste,image=self.image_hazardous_waste)
        self.label_hazardous_waste.grid(row=0,column=0)

        # 各类垃圾投放统计进度条
        self.progressbar_food_waste = ttk.Progressbar(self.labelframe_food_waste,value=50,bootstyle="success",length=self.progressbar_length)
        self.progressbar_food_waste.grid(row=0,column=1)
        self.progressbar_recyclable_waste = ttk.Progressbar(self.labelframe_recyclable_waste,value=50,bootstyle="primary",length=self.progressbar_length)
        self.progressbar_recyclable_waste.grid(row=0,column=1)
        self.progressbar_other_waste = ttk.Progressbar(self.labelframe_other_waste,value=50,bootstyle="secondary",length=self.progressbar_length)
        self.progressbar_other_waste.grid(row=0,column=1)
        self.progressbar_hazardous_waste = ttk.Progressbar(self.labelframe_hazardous_waste,value=50,bootstyle="danger",length=self.progressbar_length)
        self.progressbar_hazardous_waste.grid(row=0,column=1)

        # 各类垃圾投放进度条数值
        self.label_food_waste = ttk.Label(self.labelframe_food_waste,text='0',bootstyle="success")
        self.label_food_waste.grid(row=0,column=2)
        self.label_recyclable_waste = ttk.Label(self.labelframe_recyclable_waste,text='0',bootstyle="primary")
        self.label_recyclable_waste.grid(row=0,column=2)
        self.label_other_waste = ttk.Label(self.labelframe_other_waste,text='0',bootstyle="secondary")
        self.label_other_waste.grid(row=0,column=2)
        self.label_hazardous_waste = ttk.Label(self.labelframe_hazardous_waste,text='0',bootstyle="danger")
        self.label_hazardous_waste.grid(row=0,column=2)

        # 分隔线
        self.separator_status = ttk.Separator(self.labelframe_total,bootstyle='info',orient=VERTICAL)
        self.separator_status.grid(row=0, column=1,rowspan=4,sticky='news')

        # 各类垃圾箱状态
        self.button_food_waste_status = ttk.Button(self.labelframe_total,text='OK',bootstyle="success-outline",width=10)
        self.button_food_waste_status.grid(row=0,column=2,padx=5,pady=20,ipadx=2,ipady=2,sticky='news')
        self.button_recyclable_waste_status = ttk.Button(self.labelframe_total,text='OK',bootstyle="success-outline")
        self.button_recyclable_waste_status.grid(row=1,column=2,padx=5,pady=20,ipadx=2,ipady=2,sticky='news')
        self.button_other_waste_status = ttk.Button(self.labelframe_total,text='OK',bootstyle="success-outline")
        self.button_other_waste_status.grid(row=2,column=2,padx=5,pady=20,ipadx=2,ipady=2,sticky='news')
        self.button_hazardous_waste_status = ttk.Button(self.labelframe_total,text='OK',bootstyle="success-outline")
        self.button_hazardous_waste_status.grid(row=3,column=2,padx=5,pady=20,ipadx=2,ipady=2,sticky='news')
    
    # 视频框
    def create_video_frame(self):

        # 视频框
        self.labelframe_video = ttk.Labelframe(self.root, text="Video")
        self.labelframe_video.grid(row=0,rowspan=2,column=1,columnspan=1,padx=1,pady=1,ipadx=2,ipady=2,sticky='news')

        # 视频画布
        self.canvas_video = ttk.Canvas(self.labelframe_video, width=self.image_width, height=self.image_height)
        self.canvas_video.grid(row=0, column=0,rowspan=2,columnspan=4,sticky='news')

        # 帧率仪表盘
        self.meter_fps = ttk.Meter(
            master=self.labelframe_video,
            bootstyle='success',
            metersize=150,
            arcoffset=-210,
            arcrange=240,
            padding=5,
            amounttotal=100,
            amountused=10,
            subtext="FPS",
            subtextstyle="success",
            meterthickness= 25,
            stripethickness= 5,
        )
        self.meter_fps.grid(row=3, column=0,sticky='news')

        # 置信度仪表盘
        self.meter_conf = ttk.Meter(
            master=self.labelframe_video,
            bootstyle='success',
            metersize=150,
            padding=5,
            amounttotal=100,
            amountused=95.5,
            textright=" %",
            subtext="Conf",
            subtextstyle="success",
            meterthickness= 15,
        )
        self.meter_conf.grid(row=3, column=1,sticky='news')

        # 分类信息标签
        self.label_order = ttk.Label(self.labelframe_video,text='array',font=('Arial', 30),bootstyle="success")
        self.label_order.grid(row=2, column=0,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.label_class = ttk.Label(self.labelframe_video,text='classify',font=('Arial', 30),bootstyle="success")
        self.label_class.grid(row=2, column=1,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.label_num = ttk.Label(self.labelframe_video,text='number',font=('Arial', 30),bootstyle="success")
        self.label_num.grid(row=2, column=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.label_status = ttk.Label(self.labelframe_video,text='OK!',font=('Arial', 30),bootstyle="success")
        self.label_status.grid(row=2, column=3,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')


        # 本轮投放时间
        self.label_time = ttk.Label(self.labelframe_video,text='00:00:00',font=('Arial', 30),bootstyle="success")
        self.label_time.grid(row=3, column=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
    
    # 状态框
    def create_status_frame(self):

        # 状态框
        self.labelframe_status = ttk.Labelframe(self.root, text=" Status of Components")
        self.labelframe_status.grid(row=1, column=0,padx=1,pady=1,ipadx=2,ipady=2,sticky='news')
        self.label_status_camera = ttk.Label(self.labelframe_status,text='camera',font=('Arial', 30),bootstyle="success")
        self.label_status_camera.grid(row=0, column=0,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.label_status_conveyor = ttk.Label(self.labelframe_status,text='conveyor',font=('Arial', 30),bootstyle="success")
        self.label_status_conveyor.grid(row=1, column=0,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.label_status_detector = ttk.Label(self.labelframe_status,text='detector',font=('Arial', 30),bootstyle="success")
        self.label_status_detector.grid(row=2, column=0,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.label_status_compactors = ttk.Label(self.labelframe_status,text='compactors',font=('Arial', 30),bootstyle="success")
        self.label_status_compactors.grid(row=3, column=0,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')

        # 分隔线
        self.separator_status = ttk.Separator(self.labelframe_status,bootstyle='info',orient=VERTICAL)
        self.separator_status.grid(row=0, column=1,rowspan=4,sticky='news')

        # 状态指示
        self.button_camera_status = ttk.Button(self.labelframe_status,text='Working',bootstyle='success-outline',width=16)
        self.button_camera_status.grid(row=0, column=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.button_conveyor_status = ttk.Button(self.labelframe_status,text='Working',bootstyle='success-outline')
        self.button_conveyor_status.grid(row=1, column=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.button_detector_status = ttk.Button(self.labelframe_status,text='Working',bootstyle='success-outline')
        self.button_detector_status.grid(row=2, column=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.button_compactors_status = ttk.Button(self.labelframe_status,text='Working',bootstyle='success-outline')
        self.button_compactors_status.grid(row=3, column=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
    
    # 系统信息框
    def create_system_frame(self):

        # 系统信息框
        self.labelframe_system = ttk.Labelframe(self.root, text="System")
        self.labelframe_system.grid(row=1, column=2,padx=1,pady=1,ipadx=2,ipady=2,sticky='news')

        # CPU仪表盘
        self.meter_cpu = ttk.Meter(
            master=self.labelframe_system,
            bootstyle='success',
            metersize=self.metersize,
            arcoffset=-210,
            arcrange=240,
            padding=5,
            amounttotal=100,
            amountused=20.0,
            textright=" %",
            subtext="CPU",
            subtextstyle="success",
            meterthickness= 25,
            stripethickness= 5,
        )
        self.meter_cpu.grid(row=0, column=0,sticky='news')

        # 温度仪表盘
        self.meter_temp = ttk.Meter(
            master=self.labelframe_system,
            bootstyle='danger',
            metersize=self.metersize,
            arcoffset=-225,
            arcrange=90,
            padding=5,
            amounttotal=100,
            amountused=46.0,
            textright="°C",
            subtext="Temp",
            subtextstyle="danger",
            meterthickness= 20
        )
        self.meter_temp.grid(row=1, column=0,sticky='news')

        # 内存标签框
        self.labelframe_memory = ttk.LabelFrame(self.labelframe_system,text='Memory',bootstyle="info")
        self.labelframe_memory.grid(row=2, column=0,columnspan=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')

        # 磁盘标签框
        self.labelframe_disk = ttk.LabelFrame(self.labelframe_system,text='Disk',bootstyle="info")
        self.labelframe_disk.grid(row=3, column=0,columnspan=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')

        # 内存占用条
        self.progressbar_memory = ttk.Progressbar(
            master=self.labelframe_memory,
            bootstyle='info',
            orient='horizontal',
            value=50,
            length=self.progressbar_length,
            mode='determinate',
            )
        self.progressbar_memory.grid(row=0, column=0,sticky='news')

        # 磁盘占用条
        self.progressbar_disk = ttk.Progressbar(
            master=self.labelframe_disk,
            bootstyle='info',
            orient='horizontal',
            value=50,
            length=self.progressbar_length,
            mode='determinate',
            )
        self.progressbar_disk.grid(row=0, column=0,sticky='news')

        # 内存占用进度条数值
        self.label_memory= ttk.Label(self.labelframe_memory,text='50',bootstyle="info")
        self.label_memory.grid(row=0,column=1,sticky='news')

        # 磁盘占用进度条数值
        self.label_disk = ttk.Label(self.labelframe_disk,text='50',bootstyle="info")
        self.label_disk.grid(row=0,column=1,sticky='news')
    
    def compressor_work(self):
        barrier_dis = self.ultrasonic.get_distance() # 获取当前障碍物的距离
        filtered_dis = self.meanFilter.update(barrier_dis) # 均值滤波得到滤波后结果  
        self.ultrasonic.print_time()
        print(f"当前距离: {filtered_dis:.2f} cm")  

        if self.compressor_work_status == 0:

            # 当测得距离小于安全距离时，进行压缩  
            if filtered_dis < self.safe_dis:  
                self.button_recyclable_waste_status.config(text='FULL!!!',bootstyle='danger-outline')
                self.button_conveyor_status.config(text='STOP',bootstyle='danger-outline')
                track_stop() # 传送带停止
                self.button_camera_status.config(text='Get Ready',bootstyle='success-outline')
                gimbal_reset() # 舵机复位
                self.button_compactors_status.config(text='Working',bootstyle='warning-outline')
                self.compressor_work_status = 1 # 压缩机构设为压缩状态
                self.compressor_t1 = time.time()
                start_compress()
            # else:  
            #     print("垃圾桶内空间足够，无需压缩")  
        
        else:
            if time.time() - self.compressor_t1 >= 2 * self.time_to_run + 0.5:
                stop_compress()
                self.compressor_work_status = 0
                self.button_compactors_status.config(text='get ready',bootstyle='success-outline')
                self.button_recyclable_waste_status.config(text='OK',bootstyle='success-outline')
                self.button_conveyor_status.config(text='working',bootstyle='success-outline')
                track_start()
            elif time.time() - self.compressor_t1 >= self.time_to_run + 0.5:
                reset_compress()
            elif time.time() - self.compressor_t1 >= self.time_to_run:
                stop_compress()
        
    def get_pi_system_info(self):
        # CPU informatiom
        CPU_temp = pi_system.getCPUtemperature()
        CPU_usage = pi_system.getCPUuse()
        
        # RAM information
        RAM_stats = pi_system.getRAMinfo()
        RAM_total = int(RAM_stats[0]) 
        RAM_used = int(RAM_stats[1])
        
        RAM_perc = round(RAM_used/RAM_total * 100,1)
        
        # Disk information
        DISK_stats = pi_system.getDiskSpace()
        DISK_perc = DISK_stats[3]
        DISK_perc = DISK_perc[:-1]
        DISK_perc = float(DISK_perc)

        # Update info
        self.meter_cpu.configure(amountused = CPU_usage)
        self.meter_temp.configure(amountused = CPU_temp)
        self.progressbar_memory.configure(value = RAM_perc)
        self.progressbar_disk.configure(value = DISK_perc)
        self.label_memory.configure(text= RAM_perc)
        self.label_disk.configure(text= DISK_perc)
    #定时刷新
    def update_frame(self):

        time_start = time.time()

        ret, camframe = self.camera.read()# cv读取摄像头
        camframe = cv2.flip(camframe, 1) # 反转图像


        if self.mode and  ((time.time() - self.mode_t1) > self.mode_transfrom_time):
            self.mode = 0
        
        # 获取摄像头或视频帧
        if not self.mode:
            for _ in range(int(self.speed)):  # 根据倍速跳过或重复读取帧
                ret, frame = self.video.read()
            if not ret:  # 如果视频播放完毕
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重置视频到开头
                self.root.after(1, self.update_frame)  # 每1毫秒更新一次图像  # 跳过本次循环，重新读取帧
        else:
            frame = camframe

            
        
        # 将 camframe 修剪为 1080x1080，保持中心不变
        height, width = camframe.shape[:2]
        min_dim = min(height, width)  # 获取最小边长
        start_x = (width - min_dim) // 2  # 计算裁剪区域的起始 x 坐标
        start_y = (height - min_dim) // 2  # 计算裁剪区域的起始 y 坐标
        cropped_frame = camframe[start_y:start_y + min_dim, start_x:start_x + min_dim]  # 裁剪为中心正方形
        # resized_frame = cv2.resize(cropped_frame, (1080, 1080), interpolation=cv2.INTER_LANCZOS4)  # 缩放为 1080x1080

        # 运行模型
        results = self.cls_ncnn_model.predict(
            source=cropped_frame,  # 使用修剪后的帧
            imgsz=224,
            device="cpu",
            conf=0.25
        )  # 模型推理(预测)


        self.compressor_work()

        if self.system_status == 0 and self.compressor_work_status == 0:
            # 系统处于等待检测状态
            if results[0].probs.top1 != 0 :
                self.waste_exist_frame += 1
                self.mean_conf += results[0].probs.top1conf.item()
                for i in range(self.waste_exist_frame_max-1):
                    ret, camframe = self.camera.read()# cv读取摄像头
                    camframe = cv2.flip(camframe, 1) # 反转图像
                    # 将 camframe 修剪为 1080x1080，保持中心不变
                    height, width = camframe.shape[:2]
                    min_dim = min(height, width)  # 获取最小边长
                    start_x = (width - min_dim) // 2  # 计算裁剪区域的起始 x 坐标
                    start_y = (height - min_dim) // 2  # 计算裁剪区域的起始 y 坐标
                    cropped_frame = camframe[start_y:start_y + min_dim, start_x:start_x + min_dim]  # 裁剪为中心正方形
                    # resized_frame = cv2.resize(cropped_frame, (1080, 1080), interpolation=cv2.INTER_LANCZOS4)  # 缩放为 1080x1080

                    # 运行模型
                    results = self.cls_ncnn_model.predict(
                        source=cropped_frame,  # 使用修剪后的帧
                        imgsz=224,
                        device="cpu",
                        conf=0.25
                    )  # 模型推理(预测)
                    if results[0].probs.top1 != 0 :
                        self.waste_exist_frame += 1
                        self.mean_conf += results[0].probs.top1conf.item()
                    
                
                if self.waste_exist_frame >= self.waste_exist_frame_max and self.mean_conf/self.waste_exist_frame_max >= self.conf_threshold:
                    self.waste_exist_frame = 0
                    self.waste_exist_flag = True  
                    self.waste_total += 1        
                    # 投放信息
                    self.label_order.config(text=str(self.waste_total),bootstyle='success') 
                    self.label_class.config(text=self.wastes_cls[results[0].probs.top1],bootstyle='success')
                    self.label_num.config(text='1',bootstyle='success')
                    self.label_status.config(text='OK!',bootstyle='success')
                    # 置信率
                    conf_value = round(results[0].probs.top1conf.item() * 100,1)
                    self.meter_conf.configure(amountused = conf_value) 
                    # 更新历史信息
                    self.tableview_history.insert_row(0,(self.waste_total,self.wastes_cls[results[0].probs.top1],1,'OK!'))
                    self.tableview_history.load_table_data()
                    # 更新统计条
                    self.waste_count[results[0].probs.top1-1] += 1
                    self.progressbar_food_waste.configure(value=int(self.waste_count[0]/self.waste_total*100))
                    self.progressbar_hazardous_waste.configure(value=int(self.waste_count[1]/self.waste_total*100))
                    self.progressbar_other_waste.configure(value=int(self.waste_count[2]/self.waste_total*100))
                    self.progressbar_recyclable_waste.configure(value=int(self.waste_count[3]/self.waste_total*100))
                    self.label_food_waste.configure(text= self.waste_count[0])
                    self.label_hazardous_waste.configure(text= self.waste_count[1])
                    self.label_other_waste.configure(text= self.waste_count[2])
                    self.label_recyclable_waste.configure(text= self.waste_count[3])
                self.waste_exist_frame = 0
                self.mean_conf = 0
                print(results[0].probs.top1)
            
            if self.waste_exist_flag:
                # 垃圾存在
                    # 传送带停止工作
                self.button_conveyor_status.config(text='stop',bootstyle='danger-outline')
                track_stop()
                # 舵机倾倒垃圾
                self.button_camera_status.config(text='working',bootstyle='warning-outline')
                t2 = time.time()
                gimbal_work(results[0].probs.top1-1)
                print("time_work:",time.time() - t2) 
                self.duoji_start_time = time.time() # 获取舵机开始倾倒时间

                # 系统切换至垃圾倾倒状态
                self.system_status = 1

                # 切换画面到摄像头
                self.mode = 1
                self.mode_t1 = time.time()

        elif self.system_status == 1:
            # 系统处于垃圾倾倒状态
            if time.time() - self.duoji_start_time >= 0.5 :
                    # 舵机工作时间大于3秒，舵机置位
                    t1 = time.time()
                    gimbal_reset()
                    print("time_reset:",time.time() - t1) 
                    if time.time() - self.duoji_start_time >= 1.0 :
                        # 舵机就位，垃圾倾倒完毕
                        self.button_camera_status.config(text='get ready',bootstyle='success-outline')
                        # 清除垃圾存在标志
                        self.waste_exist_flag = False
                        self.label_order.config(text='---',bootstyle='warning')
                        self.label_class.config(text=self.wastes_cls[0],bootstyle='warning')
                        self.label_status.config(text='---',bootstyle='warning')
                        self.label_num.config(text='---',bootstyle='warning')
                        
                    
                        # 传送带重新工作
                        self.button_conveyor_status.config(text='working',bootstyle='success-outline')
                        track_start()
                        # 系统切换到等待检测状态
                        self.system_status = 0

        # 计算FPS
        self.time_stamp = time.time()
        loop_time = self.time_stamp - self.last_time_stamp
        self.last_time_stamp = self.time_stamp
        self.FPS = int(1 / loop_time)
        print("loop_time:",loop_time)

        # 更新仪表盘(每120帧更新一次)
        if self.frames_count % self.num_frames == 0:
            self.frames_count = 1
            self.meter_fps.configure(amountused=self.FPS)  
            self.get_pi_system_info()  
        else :
            self.frames_count += 1
        
        # gui.tableview_history.insert_row(0,('test',1))
        # gui.tableview_history.load_table_data()
    
        # 在图像左上角添加FPS文本
        fps_text = f"FPS: {self.FPS:.2f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        text_color = (0, 255, 0)  # 绿色
        text_position = (10, 30)  # 左上角位置
        cv2.putText(frame, fps_text, text_position, font, font_scale, text_color, font_thickness)

        if self.mode == 1:
            # 计算本轮投放时间
            count_time = get_elapsed_time(self.mode_t1)
            self.label_time.configure(text= count_time)
        else :
            self.label_time.configure(text= "00:00'00")


        # 将图像转换为tkinter格式
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 转换为RGB格式
        pillow_image = Image.fromarray(rgb_image) # 转换为Pillow格式
        resize_image = pillow_image.resize(( self.image_width, self.image_height), Image.LANCZOS)# 调整图像尺寸以适应tkinter窗口
        tk_image = ImageTk.PhotoImage(image=resize_image)# 将图像转换为tkinter格式，并存入静态变量中
        
        # 显示图像
        self.canvas_video.create_image(0, 0, anchor='nw', image=tk_image) # 显示图像
        self.static_image_container = tk_image # 将图像转换为tkinter格式，并存入静态变量中

        

        self.root.after(1, self.update_frame)  # 每1毫秒更新一次图像

    # 终止程序
    def shutdown(self):
        self.camera.release() # 释放摄像头
        self.video.release() # 释放视频
        gimbal_deinit() # 释放舵机
        track_stop() # 停止传送带
        self.root.destroy() # 销毁窗口
        
    
gui = GUI() 

#窗口全屏，绑定ESC退出，运行窗口循环
gui.root.attributes("-fullscreen", True)
gui.root.bind("<Escape>", lambda d:gui.shutdown())
gui.root.mainloop()
