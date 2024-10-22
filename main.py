from PIL import Image, ImageTk  # 图像控件

import cv2
import tkinter as tk
import threading
import time
import gpiozero

IsRunning = threading.Event()

image_width = 600
image_height = 500

image_container = None
static_image_container = None

class CameraThread(threading.Thread):
    
    #instance = 0
    def __init__(self):
        threading.Thread.__init__(self)
        #CameraThread.instance += 1
        print("启动摄像头...")
        self.camera = cv2.VideoCapture(0) # cv初始化摄像头    
        print("摄像头启动成功")
        self._IsRunning =True

    def run(self):
        global image_container
        while True:
            if self._IsRunning:
                ret, frame = self.camera.read()
                frame = cv2.flip(frame, 1)
                cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pilImage = Image.fromarray(cvimage)
                pilImage = pilImage.resize((image_width, image_height), Image.LANCZOS)
                image_container = ImageTk.PhotoImage(image=pilImage)

            else:
                self.camera.release()
                print("摄像头关闭成功")
                break
    def stop(self):
        self._IsRunning = False




class GPIOThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print("启动GPIO...")
        self.gpio18 = gpiozero.LED(18)
        print("GPIO启动成功")
        self._IsRunning =True
    
    def run(self):
        while True:
            if self._IsRunning:
                self.gpio18.on()
                time.sleep(1)
                self.gpio18.off()
                time.sleep(1) 
            else:
                break
    def stop(self):
        self._IsRunning = False
gpio_thread = GPIOThread()
camera_thread = CameraThread()

camera_thread.start()
gpio_thread.start()


root = tk.Tk()  #tk创建窗口
root.title("YFENG") 

canvas = tk.Canvas(root, bg='white', width=image_width, height=image_height)
canvas.grid(row=0, column=0)

def shutdown():
    camera_thread.stop()
    #gpio_thread.stop()
    root.destroy() 

def update_frame():
    global static_image_container,image_container
    static_image_container = image_container
    canvas.create_image(0, 0, anchor='nw', image=static_image_container)
    root.after(10, update_frame)  # 每10毫秒更新一次图像
root.after(10, update_frame)


root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda d:shutdown())
root.mainloop()
