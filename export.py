from ultralytics import YOLO

# Load a YOLO11n PyTorch model
model = YOLO("model/yolo11n_det_320.pt")

# Export the model to NCNN format
model.export(format="ncnn",imgsz=320)  # creates 'yolo11n_ncnn_model'
