import tkinter as tk
from PIL import Image, ImageTk  # 图像控件
import cv2
import gpiozero
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
ncnn_model = YOLO("yolo11n.pt")
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
show_message.set("?类垃圾 旧电池 x? 回收成功")
text_message = tk.Label(show_message_frame,textvariable=show_message,background="white", font=("Arial", 10),height=10,width=110)
text_message.grid()

#定时刷新
def update_frame():
    global static_image_container
    if mode == "Standby":
        ret, frame = video.read()
        cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
        pilImage = Image.fromarray(cvimage)
        pilImage = pilImage.resize(( image_width, image_height), Image.LANCZOS)

        static_image_container = ImageTk.PhotoImage(image=pilImage)
        canvas.create_image(0, 0, anchor='nw', image=static_image_container)
    else:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1) 
        cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
        pilImage = Image.fromarray(cvimage)
        pilImage = pilImage.resize(( image_width, image_height), Image.LANCZOS)

        static_image_container = ImageTk.PhotoImage(image=pilImage)
        results = ncnn_model(frame)
        print(results)
        text_message
        canvas.create_image(0, 0, anchor='nw', image=static_image_container)
    root.after(10, update_frame)  # 每10毫秒更新一次图像
root.after(10, update_frame)



def shutdown():
    camera.release()
    video.release()
    root.destroy()
#窗口全屏，绑定ESC退出，运行窗口循环
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda d:shutdown())
root.mainloop()
