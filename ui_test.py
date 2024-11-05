import time
import gpiozero
from PIL import Image, ImageTk  # 图像控件
Image.CUBIC = Image.BICUBIC # 显式修复ttk包bug
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import cv2
from ultralytics import YOLO

#模式
mode = None

#模型标志
model_flag = 0

#推理次数
model_count = 10

#摄像头图片参数
image_width = 1920
image_height = 1080

#静态图片防止闪烁
static_image_container = None



# #载入模型
# print("载入模型...")
# cls_ncnn_model = YOLO("model/yolo11n_cls_224_ncnn_model",task='classify')
# det_ncnn_model = YOLO("model\yolo11n_det_320_ncnn_model",task='detect')
# print("模型载入完毕")

#启动摄像头（较费时），载入视频
print("启动摄像头...")
camera = cv2.VideoCapture(0) # cv初始化摄像头  
video = cv2.VideoCapture("Video.mp4")# cv初始化视频
print("摄像头启动成功")

class GUI:
    '''界面类'''
    def __init__(self):
        '''初始化界面'''
        # 创建窗口
        self.root = ttk.Window()

        # 设置风格字体
        self.style = ttk.Style("litera")
        font = ("Arial",12)
        self.style.configure('TLabelframe.Label', font=font)
        self.style.configure('custom.primary.Treeview.Heading', font=('Arial', 15))  # 设置表头字体
        self.style.configure('custom.primary.Treeview',rowheight=80, font=('Arial', 15))

        # 各类属性
        self.tableview_items_num = 15
        self.progressbar_length = 1000
        self.tableview_column_width = 200
        self.image_width = image_width
        self.image_height = image_height

        # 读取各类垃圾图标
        self.image_food_waste = ImageTk.PhotoImage(Image.open("gui_images/food_waste_logo.png").resize((100,100)))
        self.image_recyclable_waste = ImageTk.PhotoImage(Image.open("gui_images/recyclable_waste_logo.png").resize((100,100)))
        self.image_other_waste = ImageTk.PhotoImage(Image.open("gui_images/other_waste_logo.png").resize((100,100)))
        self.image_hazardous_waste = ImageTk.PhotoImage(Image.open("gui_images/hazardous_waste_logo.png").resize((100,100)))

        # 界面编写
        self.interface()

    def interface(self):
        '''界面编写'''
        self.create_history_frame()
        self.create_total_frame()
        self.create_video_frame()
        self.create_status_frame()
        self.create_system_frame()
    def create_history_frame(self):
        '''历史记录框'''

        # 标签框
        self.labelframe_history = ttk.Labelframe(self.root, text="历史记录")
        self.labelframe_history.grid(row=0, column=0,rowspan=1,padx=1,pady=1,ipadx=2,ipady=2)

        # 列表框
        colors = self.root.style.colors

        coldata = [
            {"text": "序号", "stretch": False,"width": self.tableview_column_width},
            {"text": "类别", "stretch": False,"width": self.tableview_column_width},
            {"text": "数量", "stretch": False,"width": self.tableview_column_width},
            {"text": "状态", "stretch": False,"width": self.tableview_column_width}
            
        ]

        rowdata = [
            ('其他垃圾',1,1,1),
            ('有害垃圾',2),
            ('其他垃圾',1),
            ('有害垃圾',2),
            ('其他垃圾',1),
            ('有害垃圾',2),
            ('其他垃圾',1),
            ('有害垃圾',2)
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

    def create_total_frame(self):
        '''投放统计框'''
        # 标签框
        self.labelframe_total = ttk.Labelframe(self.root, text="投放统计")
        self.labelframe_total.grid(row=1, column=1,rowspan=1,padx=1,pady=1,ipadx=2,ipady=2,sticky='news')

        # 各类垃圾标签框
        self.labelframe_food_waste = ttk.Labelframe(self.labelframe_total,text='厨余垃圾',bootstyle="success")
        self.labelframe_food_waste.grid(row=0,column=0,padx=5,pady=5,ipadx=2,ipady=2)
        self.labelframe_recyclable_waste = ttk.Labelframe(self.labelframe_total,text='可回收物',bootstyle="primary")
        self.labelframe_recyclable_waste.grid(row=1,column=0,padx=5,pady=5,ipadx=2,ipady=2)
        self.labelframe_other_waste = ttk.Labelframe(self.labelframe_total,text='其他垃圾',bootstyle="secondary")
        self.labelframe_other_waste.grid(row=2,column=0,padx=5,pady=5,ipadx=2,ipady=2)
        self.labelframe_hazardous_waste = ttk.Labelframe(self.labelframe_total,text='有害垃圾',bootstyle="danger")
        self.labelframe_hazardous_waste.grid(row=3,column=0,padx=5,pady=5,ipadx=2,ipady=2)

        # 各类垃圾图标

        self.label_food_waste = ttk.Label(self.labelframe_food_waste,text="厨余垃圾",image=self.image_food_waste)
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
        self.label_food_waste = ttk.Label(self.labelframe_food_waste,text='50',bootstyle="success")
        self.label_food_waste.grid(row=0,column=2)
        self.label_recyclable_waste = ttk.Label(self.labelframe_recyclable_waste,text='50',bootstyle="primary")
        self.label_recyclable_waste.grid(row=0,column=2)
        self.label_other_waste = ttk.Label(self.labelframe_other_waste,text='50',bootstyle="secondary")
        self.label_other_waste.grid(row=0,column=2)
        self.label_hazardous_waste = ttk.Label(self.labelframe_hazardous_waste,text='50',bootstyle="danger")
        self.label_hazardous_waste.grid(row=0,column=2)

        # 分隔线
        self.separator_status = ttk.Separator(self.labelframe_total,bootstyle='info',orient=VERTICAL)
        self.separator_status.grid(row=0, column=1,rowspan=4,sticky='news')

        # 各类垃圾箱状态
        self.button_food_waste_status = ttk.Button(self.labelframe_total,text='正常',bootstyle="success-outline",width=10)
        self.button_food_waste_status.grid(row=0,column=2,padx=5,pady=20,ipadx=2,ipady=2,sticky='news')
        self.button_recyclable_waste_status = ttk.Button(self.labelframe_total,text='正常',bootstyle="success-outline")
        self.button_recyclable_waste_status.grid(row=1,column=2,padx=5,pady=20,ipadx=2,ipady=2,sticky='news')
        self.button_other_waste_status = ttk.Button(self.labelframe_total,text='正常',bootstyle="success-outline")
        self.button_other_waste_status.grid(row=2,column=2,padx=5,pady=20,ipadx=2,ipady=2,sticky='news')
        self.button_hazardous_waste_status = ttk.Button(self.labelframe_total,text='正常',bootstyle="success-outline")
        self.button_hazardous_waste_status.grid(row=3,column=2,padx=5,pady=20,ipadx=2,ipady=2,sticky='news')

    def create_video_frame(self):
        '''视频框'''
        # 视频框
        self.labelframe_video = ttk.Labelframe(self.root, text="视频")
        self.labelframe_video.grid(row=0, column=1,columnspan=2,padx=1,pady=1,ipadx=2,ipady=2,sticky='news')

        # 视频画布
        self.canvas_video = ttk.Canvas(self.labelframe_video, width=self.image_width, height=self.image_height)
        self.canvas_video.grid(row=0, column=0,rowspan=2,columnspan=4,sticky='news')

        # 帧率仪表盘
        self.meter_fps = ttk.Meter(
            master=self.labelframe_video,
            bootstyle='success',
            metersize=200,
            arcoffset=-210,
            arcrange=240,
            padding=5,
            amounttotal=1000,
            amountused=100,
            subtext="FPS",
            subtextstyle="success",
            meterthickness= 25,
            stripethickness= 5,
        )
        self.meter_fps.grid(row=0, column=4,sticky='news')

        # 置信度仪表盘
        self.meter_conf = ttk.Meter(
            master=self.labelframe_video,
            bootstyle='success',
            metersize=200,
            padding=5,
            amounttotal=100,
            amountused=95.5,
            textright=" %",
            subtext="置信度",
            subtextstyle="success",
            meterthickness= 15,
        )
        self.meter_conf.grid(row=1, column=4,sticky='news')

        # 分类信息标签
        self.label_order = ttk.Label(self.labelframe_video,text='投放顺序',font=('Arial', 30),bootstyle="success")
        self.label_order.grid(row=2, column=0,padx=5,pady=5,ipadx=2,ipady=2)
        self.label_class = ttk.Label(self.labelframe_video,text='垃圾类别',font=('Arial', 30),bootstyle="success")
        self.label_class.grid(row=2, column=1,padx=5,pady=5,ipadx=2,ipady=2)
        self.label_num = ttk.Label(self.labelframe_video,text='投放数量',font=('Arial', 30),bootstyle="success")
        self.label_num.grid(row=2, column=2,padx=5,pady=5,ipadx=2,ipady=2)

        # 分类状态框
        self.floodgauge_classify = ttk.Floodgauge(
            master=self.labelframe_video,
            bootstyle="success",
            length=400,
            font=("Arial", 30),
            mask="分类完成",
            mode="determinate",
            )
        self.floodgauge_classify.grid(row=2, column=3,padx=5,pady=5,ipadx=2,ipady=2)
        self.floodgauge_classify.start()


        # 本轮投放时间
        self.label_num = ttk.Label(self.labelframe_video,text='00:00:00',font=('Arial', 30),bootstyle="success")
        self.label_num.grid(row=2, column=4,padx=5,pady=5,ipadx=2,ipady=2)
        
    def create_status_frame(self):
        '''状态框'''
        # 状态框
        self.labelframe_status = ttk.Labelframe(self.root, text="状态")
        self.labelframe_status.grid(row=1, column=0,padx=1,pady=1,ipadx=2,ipady=2,sticky='news')

        self.label_status_camera = ttk.Label(self.labelframe_status,text='摄像头状态',font=('Arial', 30),bootstyle="success")
        self.label_status_camera.grid(row=0, column=0,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.label_status_conveyor = ttk.Label(self.labelframe_status,text='传送带状态',font=('Arial', 30),bootstyle="success")
        self.label_status_conveyor.grid(row=1, column=0,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.label_status_detector = ttk.Label(self.labelframe_status,text='检测器状态',font=('Arial', 30),bootstyle="success")
        self.label_status_detector.grid(row=2, column=0,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.label_status_compactors = ttk.Label(self.labelframe_status,text='压缩器状态',font=('Arial', 30),bootstyle="success")
        self.label_status_compactors.grid(row=3, column=0,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')


        # 分隔线
        self.separator_status = ttk.Separator(self.labelframe_status,bootstyle='info',orient=VERTICAL)
        self.separator_status.grid(row=0, column=1,rowspan=4,sticky='news')

        # 状态指示
        self.button_camera_status = ttk.Button(self.labelframe_status,text='工作中',bootstyle='success-outline',width=16)
        self.button_camera_status.grid(row=0, column=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.button_conveyor_status = ttk.Button(self.labelframe_status,text='工作中',bootstyle='success-outline')
        self.button_conveyor_status.grid(row=1, column=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.button_detector_status = ttk.Button(self.labelframe_status,text='工作中',bootstyle='success-outline')
        self.button_detector_status.grid(row=2, column=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')
        self.button_compactors_status = ttk.Button(self.labelframe_status,text='工作中',bootstyle='success-outline')
        self.button_compactors_status.grid(row=3, column=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')

    def create_system_frame(self):
        '''系统信息框'''
        # 系统信息框
        self.labelframe_system = ttk.Labelframe(self.root, text="系统信息")
        self.labelframe_system.grid(row=1, column=2,padx=1,pady=1,ipadx=2,ipady=2,sticky='news')

        # CPU仪表盘
        self.meter_cpu = ttk.Meter(
            master=self.labelframe_system,
            bootstyle='success',
            metersize=200,
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
            metersize=200,
            arcoffset=-225,
            arcrange=90,
            padding=5,
            amounttotal=100,
            amountused=46.0,
            textright=" ℃",
            subtext="温度",
            subtextstyle="danger",
            meterthickness= 20
        )
        self.meter_temp.grid(row=0, column=1,sticky='news')

        # 内存标签框
        self.labelframe_memory = ttk.LabelFrame(self.labelframe_system,text='内存',bootstyle="info")
        self.labelframe_memory.grid(row=1, column=0,columnspan=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')

        # 磁盘标签框
        self.labelframe_disk = ttk.LabelFrame(self.labelframe_system,text='磁盘',bootstyle="info")
        self.labelframe_disk.grid(row=2, column=0,columnspan=2,padx=5,pady=5,ipadx=2,ipady=2,sticky='news')


        # 内存占用条
        self.progressbar_memory = ttk.Progressbar(
            master=self.labelframe_memory,
            bootstyle='info',
            orient='horizontal',
            value=50,
            length=600,
            mode='determinate',
            )
        self.progressbar_memory.grid(row=0, column=0,sticky='news')

        # 磁盘占用条
        self.progressbar_disk = ttk.Progressbar(
            master=self.labelframe_disk,
            bootstyle='info',
            orient='horizontal',
            value=50,
            length=600,
            mode='determinate',
            )
        self.progressbar_disk.grid(row=0, column=0,sticky='news')

        # 内存占用进度条数值
        self.label_memory= ttk.Label(self.labelframe_memory,text='50',bootstyle="info")
        self.label_memory.grid(row=0,column=1,sticky='news')

        # 磁盘占用进度条数值
        self.label_disk = ttk.Label(self.labelframe_disk,text='50',bootstyle="info")
        self.label_disk.grid(row=0,column=1,sticky='news')




gui = GUI()





#定时刷新
def update_frame():
    global static_image_container
    global model_flag
    global model_count

    # if model_count <= 0:
    #     model_flag = 1^model_flag # 切换模型
    #     print(model_flag)
    #     if model_flag == 0:
    #         model_count = 30
    #     else:
    #         model_count = 0
    # else:
    #     model_count = model_count - 1


    if mode == "Standby":
        ret, frame = video.read()
    else:
        loop_start = cv2.getTickCount()
        
        ret, frame = camera.read()# cv读取摄像头
        frame = cv2.flip(frame, 1) # 反转图像
        annotated_frame = None
        
        # if model_flag == 1:
        #     results = det_ncnn_model.predict(
        #             source=frame,imgsz=320,device="cpu",iou=0.5,
        #             conf=0.25,max_det=3
        #             )# 模型推理(预测)
        #     annotated_frame = results[0].plot()# 绘制预测结果
        # else:
        #     results = cls_ncnn_model.predict(
        #             source=frame,imgsz=224,device="cpu",iou=0.5,
        #             conf=0.25,max_det=3
        #             )# 模型推理(预测)
        annotated_frame = frame
        '''
        results = ncnn_model.track(
            source=frame,imgsz=480,device="cpu",iou=0.5,
            conf=0.25,max_det=1,persist=True,tracker="bytetrack.yaml"
            )#模型推理(跟踪)
        '''

        # 计算FPS
        loop_end = cv2.getTickCount()
        loop_time = loop_end - loop_start
        total_time = loop_time / (cv2.getTickFrequency())
        FPS = int(1 / total_time)

        gui.meter_fps.configure(amountused=FPS)
        gui.floodgauge_classify.step(1)
        # gui.tableview_history.insert_row(0,('test',1))
        # gui.tableview_history.load_table_data()
        
        # 在图像左上角添加FPS文本
        fps_text = f"FPS: {FPS:.2f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        text_color = (0, 255, 0)  # 绿色
        text_position = (10, 30)  # 左上角位置
        cv2.putText(annotated_frame, fps_text, text_position, font, font_scale, text_color, font_thickness)

        
    cvimage = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB) 
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize(( image_width, image_height), Image.LANCZOS)# 调整图像尺寸以适应tkinter窗口
    static_image_container = ImageTk.PhotoImage(image=pilImage)# 将图像转换为tkinter格式，并存入静态变量中
    gui.canvas_video.create_image(0, 0, anchor='nw', image=static_image_container) # 显示图像
    gui.root.after(100, update_frame)  # 每100毫秒更新一次图像
update_frame() # 启动更新函数


def shutdown():
    camera.release() # 释放摄像头
    video.release() # 释放视频
    gui.root.destroy() # 销毁窗口

#窗口全屏，绑定ESC退出，运行窗口循环
gui.root.attributes("-fullscreen", True)
gui.root.bind("<Escape>", lambda d:shutdown())
gui.root.mainloop()
