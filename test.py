import time
import gpiozero
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from PIL import Image, ImageTk  # 图像控件
import cv2
from ultralytics import YOLO

# 模式
mode = None

# 模型标志
model_flag = 0

# 推理次数
model_count = 10

# 摄像头图片参数
p_w_h = 16 / 9
image_width = 2000
image_height = int(image_width / p_w_h)

# 静态图片防止闪烁
static_image_container = None


# #载入模型
# print("载入模型...")
# cls_ncnn_model = YOLO("model/yolo11n_cls_224_ncnn_model",task='classify')
# det_ncnn_model = YOLO("model\yolo11n_det_320_ncnn_model",task='detect')
# print("模型载入完毕")

# 启动摄像头（较费时），载入视频
print("启动摄像头...")
camera = cv2.VideoCapture(0)  # cv初始化摄像头
video = cv2.VideoCapture("Video.mp4")  # cv初始化视频
print("摄像头启动成功")

font = ("Arial", 12)

# 创建窗口
root = ttk.Window()
style = ttk.Style("litera")
style.configure("TLabelframe.Label", font=font)
# style = ttk.Style("darkly")


# 列表框
list_messages = ["msg1", "msg2", "msg3"]
list_frame = ttk.LabelFrame(root, text="历史记录", bootstyle="info")
list_frame.grid(row=0, column=0, rowspan=3, padx=1, pady=1, ipadx=2, ipady=2)
colors = root.style.colors

coldata = [
    {"text": "投放垃圾", "stretch": False, "width": 300},
    {"text": "投放顺序", "stretch": False, "width": 300},
]

rowdata = [
    ("其他垃圾", 1),
    ("有害垃圾", 2),
    ("其他垃圾", 1),
    ("有害垃圾", 2),
    ("其他垃圾", 1),
    ("有害垃圾", 2),
    ("其他垃圾", 1),
    ("有害垃圾", 2),
]
dt = Tableview(
    master=list_frame,
    coldata=coldata,
    rowdata=rowdata,
    paginated=False,
    searchable=False,
    bootstyle=PRIMARY,
    stripecolor=(colors.light, None),
    height=60,
)
dt.grid()
# listbox = tk.Listbox(list_frame, height=75, width=50)
# for item in list_messages:
#     listbox.insert('end',item)
# listbox.grid()

# 视频框
vedio_frame = ttk.LabelFrame(root, text="视频区", bootstyle="success")
vedio_frame.grid(row=0, column=1, columnspan=2, sticky="news", padx=1, pady=1)
canvas = ttk.Canvas(vedio_frame, bg="white", height=image_height, width=image_width)
canvas.grid()

# 文本框
show_message_frame = ttk.LabelFrame(root, text="分类信息区", bootstyle="info")
show_message_frame.grid(row=1, column=1, columnspan=2, sticky="news", padx=1, pady=1)

show_message = tk.StringVar()
show_message.set("ex:1类垃圾 旧电池 x1 回收成功")

text_message = tk.Label(
    show_message_frame,
    textvariable=show_message,
    background="white",
    font=font,
)
text_message.grid()

# 进度框
progress_frame = ttk.LabelFrame(root, text="投放累计", bootstyle="warning")
progress_frame.grid(row=2, column=1, columnspan=2, sticky="news", padx=1, pady=1)

# 各类垃圾标签
labelframe_food_waste = ttk.Labelframe(
    progress_frame, text="厨余垃圾", bootstyle="success"
)
labelframe_food_waste.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2)
labelframe_recyclable_waste = ttk.Labelframe(
    progress_frame, text="可回收垃圾", bootstyle="primary"
)
labelframe_recyclable_waste.grid(row=1, column=0, padx=5, pady=5, ipadx=2, ipady=2)
labelframe_other_waste = ttk.Labelframe(
    progress_frame, text="其他垃圾", bootstyle="secondary"
)
labelframe_other_waste.grid(row=2, column=0, padx=5, pady=5, ipadx=2, ipady=2)
labelframe_hazardous_waste = ttk.Labelframe(
    progress_frame, text="有害垃圾", bootstyle="danger"
)
labelframe_hazardous_waste.grid(row=3, column=0, padx=5, pady=5, ipadx=2, ipady=2)

# 各类垃圾投放进度条
progress_food_waste = ttk.Progressbar(
    labelframe_food_waste, value=50, bootstyle="success", length=1400
)
progress_food_waste.grid()
progress_recyclable_waste = ttk.Progressbar(
    labelframe_recyclable_waste, value=50, bootstyle="primary", length=1400
)
progress_recyclable_waste.grid()
progress_other_waste = ttk.Progressbar(
    labelframe_other_waste, value=50, bootstyle="secondary", length=1400
)
progress_other_waste.grid()
progress_hazardous_waste = ttk.Progressbar(
    labelframe_hazardous_waste, value=50, bootstyle="danger", length=1400
)
progress_hazardous_waste.grid()

# 各类垃圾投放进度条数值
label_food_waste = ttk.Label(labelframe_food_waste, text="50", bootstyle="success")
label_food_waste.grid(row=0, column=1)
label_recyclable_waste = ttk.Label(
    labelframe_recyclable_waste, text="50", bootstyle="primary"
)
label_recyclable_waste.grid(row=0, column=1)
label_other_waste = ttk.Label(labelframe_other_waste, text="50", bootstyle="secondary")
label_other_waste.grid(row=0, column=1)
label_hazardous_waste = ttk.Label(
    labelframe_hazardous_waste, text="50", bootstyle="danger"
)
label_hazardous_waste.grid(row=0, column=1)


# 定时刷新
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

        ret, frame = camera.read()  # cv读取摄像头
        frame = cv2.flip(frame, 1)  # 反转图像
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
        """
        results = ncnn_model.track(
            source=frame,imgsz=480,device="cpu",iou=0.5,
            conf=0.25,max_det=1,persist=True,tracker="bytetrack.yaml"
            )#模型推理(跟踪)
        """

        # 计算FPS
        loop_end = cv2.getTickCount()
        loop_time = loop_end - loop_start
        total_time = loop_time / (cv2.getTickFrequency())
        FPS = int(1 / total_time)

        # 在图像左上角添加FPS文本
        fps_text = f"FPS: {FPS:.2f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        text_color = (0, 255, 0)  # 绿色
        text_position = (10, 30)  # 左上角位置
        cv2.putText(
            annotated_frame,
            fps_text,
            text_position,
            font,
            font_scale,
            text_color,
            font_thickness,
        )

    cvimage = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize(
        (image_width, image_height), Image.LANCZOS
    )  # 调整图像尺寸以适应tkinter窗口
    static_image_container = ImageTk.PhotoImage(
        image=pilImage
    )  # 将图像转换为tkinter格式，并存入静态变量中
    canvas.create_image(0, 0, anchor="nw", image=static_image_container)  # 显示图像
    root.after(100, update_frame)  # 每100毫秒更新一次图像


update_frame()  # 启动更新函数


def shutdown():
    camera.release()  # 释放摄像头
    video.release()  # 释放视频
    root.destroy()  # 销毁窗口


# 窗口全屏，绑定ESC退出，运行窗口循环
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda d: shutdown())
root.mainloop()
