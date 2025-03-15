from ultralytics import YOLO

model = YOLO("model/wasteCls_v4.pt")

model.export(format="ncnn", imgsz=224, task="classify")
