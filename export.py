from ultralytics import YOLO

model = YOLO("model/yolo11n_single_cls_224.pt")

model.export(format="ncnn", imgsz=224, task="classify")
