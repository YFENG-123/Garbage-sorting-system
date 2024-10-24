import time
import gpiozero
import tkinter as tk
from PIL import Image, ImageTk  # 图像控件
import cv2
from ultralytics import YOLO


#模式
mode = None

#摄像头图片参数
image_width = 800
image_height = 400

#静态图片防止闪烁
static_image_container = None

#载入模型
print("载入模型...")
ncnn_model = YOLO("model/yolo11n_det_320_ncnn_model",task='detect')
print("模型载入完毕")

#启动摄像头（较费时），载入视频
print("启动摄像头...")
camera = cv2.VideoCapture(0) # cv初始化摄像头  
video = cv2.VideoCapture("Video.mp4")# cv初始化视频
print("摄像头启动成功")


# 创建窗口
root = tk.Tk()  #tk创建窗口
root.title("YFENG")

# 列表框
list_messages = ["msg1","msg2","msg3"]
list_frame = tk.Frame(root,bg='green')
list_frame.grid(row=0, column=0,rowspan=3,sticky='news')
listbox = tk.Listbox(list_frame, height=50, width=25)
for item in list_messages:
    listbox.insert('end',item)
listbox.grid()

# 视频框
vedio_frame = tk.Frame(root,bg='green')
vedio_frame.grid(row=0, column=1,sticky='news')
canvas = tk.Canvas(vedio_frame, bg='white',height=image_height,width=image_width)
canvas.grid()

# 文本框
show_message_frame = tk.Frame(root,bg='green')
show_message_frame.grid(row=1, column=1,sticky='news')
show_message = tk.StringVar()
show_message.set("ex:1类垃圾 旧电池 x1 回收成功")
text_message = tk.Label(show_message_frame,textvariable=show_message,background="white", font=("Arial", 10),height=10,width=110)
text_message.grid()

#定时刷新
def update_frame():
    global static_image_container
    if mode == "Standby":
        ret, frame = video.read()
    else:
        ret, frame = camera.read()# cv读取摄像头
        frame = cv2.flip(frame, 1) # 反转图像
        results = ncnn_model.predict(
                    source=frame,imgsz=320,device="cpu",iou=0.5,
                    conf=0.25,max_det=3
                    )# 模型推理
        '''
        results = ncnn_model.track(
            source=frame,imgsz=480,device="cpu",iou=0.5,
            conf=0.25,max_det=1,persist=True,tracker="bytetrack.yaml"
            )
        '''
        annotated_frame = results[0].plot()# 绘制预测结果
    cvimage = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB) 
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize(( image_width, image_height), Image.LANCZOS)# 调整图像尺寸以适应tkinter窗口
    static_image_container = ImageTk.PhotoImage(image=pilImage)# 将图像转换为tkinter格式，并存入静态变量中
    canvas.create_image(0, 0, anchor='nw', image=static_image_container) # 显示图像
    root.after(1, update_frame)  # 每10毫秒更新一次图像
update_frame() # 启动更新函数



def shutdown():
    camera.release() # 释放摄像头
    video.release() # 释放视频
    root.destroy() # 销毁窗口

#窗口全屏，绑定ESC退出，运行窗口循环
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda d:shutdown())
root.mainloop()
