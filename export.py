from ultralytics import YOLO

# Load a YOLO11n PyTorch model
model = YOLO("yolo11n_det_480.pt")

# Export the model to NCNN format
model.export(format="ncnn",imgsz=352)  # creates 'yolo11n_ncnn_model'
