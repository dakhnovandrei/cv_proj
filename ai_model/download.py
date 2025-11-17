import os
from roboflow import Roboflow

rf = Roboflow(api_key="csrhS0RkAZwHKY4OcPgC")
project = rf.workspace("agrikheti").project("plant-disease-hgequ")
version = project.version(1)
dataset = version.download("yolov8")
print(dataset.location)
