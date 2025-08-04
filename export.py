from ultralytics import YOLO

model = YOLO("model/wasteCls_v5.pt")

model.export(format="ncnn", imgsz=224, task="classify")
