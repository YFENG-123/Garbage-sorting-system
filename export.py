from ultralytics import YOLO

model = YOLO("model\yolo11n_cls_diy_v2.pt")

model.export(format="ncnn", imgsz=224, task="classify")
