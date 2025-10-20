```pwsh
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -U ultralytics
```

```py
from ultralytics import YOLO

model = YOLO("yolo11n.pt")   # 例: Nano
results = model("path/to/image.jpg")
results[0].show()            # 可視化
```