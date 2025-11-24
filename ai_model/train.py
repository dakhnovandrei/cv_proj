from ultralytics import YOLO
import os
import multiprocessing as mp


def main():
    dataset = "C:\\Users\\User\\Desktop\\proj_1\\ai_model\\plant-disease-1"
    model = YOLO('yolo11s.pt')

    data_yaml = os.path.join(dataset, 'data.yaml')

    model.train(
        data=data_yaml,
        epochs=100,
        imgsz=640,
        batch=16,
        name='plant_disease_exp2',
        device=0,
        workers=4,
        pretrained=True
    )


if __name__ == '__main__':
    mp.freeze_support()
    main()

