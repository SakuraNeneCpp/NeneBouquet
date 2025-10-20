from ultralytics import YOLO

model = YOLO("yolo11n.pt")
results = model("recaptcha_v2.webp")
results[0].show()