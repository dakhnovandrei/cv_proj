from ultralytics import YOLO
import os
import multiprocessing as mp


def main():
    dataset = "C:\\Users\\User\\Desktop\\proj_1\\backend\\ai_model\\plant-disease-1"
    model = YOLO('C:\\Users\\User\\Desktop\\proj_1\\backend\\runs\\detect\\plant_disease_exp3\\weights\\best.pt')

    data_yaml = os.path.join(dataset, 'data.yaml')

    model.train(
        data=data_yaml,
        epochs=50,
        imgsz=640,
        batch=16,
        name='plant_disease_exp5',
        device=0,
        workers=4,
        cls=1.5
    )


if __name__ == '__main__':
    mp.freeze_support()
    main()
