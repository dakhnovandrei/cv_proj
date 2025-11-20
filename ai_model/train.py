from ultralytics import YOLO
import os
import multiprocessing as mp


def main():
    dataset = "C:\\Users\\User\\Desktop\\proj_1\\plant-disease-1"
    model = YOLO('../runs/detect/plant_disease_exp16/weights/best.pt')

    data_yaml = os.path.join(dataset, 'data.yaml')

    model.train(
        data=data_yaml,
        epochs=100,
        imgsz=640,
        batch=16,
        name='plant_disease_exp16',
        device=0,
        workers=4,
    )


if __name__ == '__main__':
    mp.freeze_support()
    main()
