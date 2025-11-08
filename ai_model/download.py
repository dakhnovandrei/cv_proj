import os
from roboflow import Roboflow

rf = Roboflow(api_key="csrhS0RkAZwHKY4OcPgC")
project = rf.workspace("zhuwujibingjiance").project("plant-diseases-detection-system")
version = project.version(18)
dataset = version.download("yolov8")
print(dataset.location)
