from ultralytics import YOLO

model = YOLO("model\yolo11n_det_320.pt")

model.export(format="ncnn", imgsz=320, task="detect")
