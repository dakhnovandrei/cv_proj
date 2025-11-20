import os
import cv2
import numpy as np
import yaml
from ultralytics import YOLO

# from src.routers.minio_client import upload_images

# Конфигурация
MODEL_PATH = '../runs/detect/plant_disease_exp162/weights/best.pt'
dataset = "C:\\Users\\User\\Desktop\\proj_1\\plant-disease-1"
DATA_YAML = os.path.join(dataset, 'data.yaml')

# Загрузка классов
with open(DATA_YAML) as f:
    CLASS_NAMES = yaml.safe_load(f)['names']

print("🎯 Загруженные классы:", CLASS_NAMES)

# Загрузка модели YOLO
model = YOLO(MODEL_PATH)
print("✅ Модель YOLO загружена успешно")


def get_image_bytes(res_image, image_format="JPEG", quality=95):
    if image_format == "JPEG":
        success, encoded_image = cv2.imencode('.jpg', res_image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    elif image_format == "PNG":
        success, encoded_image = cv2.imencode('.png', res_image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    else:
        raise ValueError(f"Неподдерживаемый тип файлов {image_format}")
    if not success:
        raise ValueError(f'Не смогли узнать вес изображения')

    return encoded_image.tobytes()


def hybrid_plant_detector(image_path, color_threshold=0.3, yolo_confidence=0.4):
    """
    Комбинированный детектор растений: YOLO + цветовая проверка
    """
    if not os.path.exists(image_path):
        print(f"❌ Файл не найден: {image_path}")
        return [], None, "FILE_NOT_FOUND"

    # Загрузка изображения
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Не удалось загрузить изображение")
        return [], None, "LOAD_ERROR"

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    original_bgr = image.copy()

    # YOLO детекция
    print("🔍 Запуск YOLO детекции...")
    results = model.predict(source=image_path, conf=yolo_confidence, imgsz=640)
    r = results[0]

    if len(r.boxes) == 0:
        print("🌿 YOLO: растения не обнаружены")
        return [], original_bgr, []

    print(f"📊 YOLO обнаружил: {len(r.boxes)} объектов")

    # Цветовая проверка каждого bbox
    detected_boxes = []
    color_stats = []

    # Диапазоны цветов растений
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    lower_yellow = np.array([20, 40, 40])
    upper_yellow = np.array([35, 255, 255])
    lower_brown = np.array([10, 40, 20])
    upper_brown = np.array([20, 255, 255])

    for i, box in enumerate(r.boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        class_name = CLASS_NAMES[cls]

        # Вырезаем регион bbox
        box_region = hsv[y1:y2, x1:x2]
        if box_region.size == 0:
            continue

        # Проверяем цветовые диапазоны
        green_mask = cv2.inRange(box_region, lower_green, upper_green)
        yellow_mask = cv2.inRange(box_region, lower_yellow, upper_yellow)
        brown_mask = cv2.inRange(box_region, lower_brown, upper_brown)

        plant_mask = cv2.bitwise_or(green_mask, yellow_mask)
        plant_mask = cv2.bitwise_or(plant_mask, brown_mask)

        plant_ratio = np.sum(plant_mask > 0) / plant_mask.size

        color_info = {
            'class': class_name,
            'confidence': conf,
            'plant_ratio': plant_ratio,
            'green_ratio': np.sum(green_mask > 0) / green_mask.size,
            'yellow_ratio': np.sum(yellow_mask > 0) / yellow_mask.size,
            'brown_ratio': np.sum(brown_mask > 0) / brown_mask.size,
            'bbox': (x1, y1, x2, y2)
        }

        print(f"📦 Объект {i + 1}: {class_name} (YOLO: {conf:.3f})")
        print(f"   🎨 Цвета: общий {plant_ratio:.1%}, зеленый {color_info['green_ratio']:.1%}")

        # Проверяем, достаточно ли растительных цветов в bbox
        if plant_ratio >= color_threshold:
            detected_boxes.append(box)
            color_stats.append(color_info)
            print(f"   ✅ Принят (цветовой критерий выполнен)")
        else:
            print(f"   ❌ Отфильтрован (мало растительных цветов)")

    print(f"\n🌿 ИТОГ: После цветовой фильтрации {len(detected_boxes)}/{len(r.boxes)} объектов")

    return detected_boxes, original_bgr, color_stats


def detection_with_minio(image_path, color_threshold=0.3):
    """
    Визуализация с использованием OpenCV (без matplotlib/Tkinter)
    """
    detected_boxes, original_bgr, color_stats = hybrid_plant_detector(image_path, color_threshold)

    result_image = original_bgr.copy()

    # Рисуем bounding boxes
    for i, box_info in enumerate(color_stats):
        x1, y1, x2, y2 = box_info['bbox']
        class_name = box_info['class']
        confidence = box_info['confidence']
        plant_ratio = box_info['plant_ratio']

        # Выбираем цвет в зависимости от типа растения
        if box_info['green_ratio'] > 0.3:
            color = (0, 255, 0)
        elif box_info['yellow_ratio'] > 0.2:
            color = (0, 255, 255)
        elif box_info['brown_ratio'] > 0.2:
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)

        # Рисуем bounding box
        cv2.rectangle(result_image, (x1, y1), (x2, y2), color, 3)

        # Подпись
        label = f"{class_name} {confidence:.2f}"
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]

        # Фон для текста
        cv2.rectangle(result_image, (x1, y1 - label_size[1] - 10),
                      (x1 + label_size[0], y1), color, -1)

        # Текст
        cv2.putText(result_image, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Дополнительная информация
        color_label = f"color:{plant_ratio:.0%}"
        cv2.putText(result_image, color_label, (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    height, width = result_image.shape[:2]
    max_width = 1200
    if width > max_width:
        scale = max_width / width
        new_width = max_width
        new_height = int(height * scale)
        result_image = cv2.resize(result_image, (new_width, new_height))

    # # Сохраняем результат
    # output_path = "detection_result.jpg"
    # cv2.imwrite(output_path, result_image)

    return result_image

# def detection_with_minio(image_path, color_threshold=0.2):
#     """
#     Простая детекция с сохранением результата (без отображения)
#     """
#     detected_boxes, original_bgr, color_stats = hybrid_plant_detector(image_path, color_threshold)
#
#     # Создаем копию для рисования
#     result_image = original_bgr.copy()
#
#     # Рисуем bounding boxes
#     for i, box_info in enumerate(color_stats):
#         x1, y1, x2, y2 = box_info['bbox']
#         class_name = box_info['class']
#         confidence = box_info['confidence']
#         plant_ratio = box_info['plant_ratio']
#
#         # Выбираем цвет в зависимости от типа растения
#         if box_info['green_ratio'] > 0.3:
#             color = (0, 255, 0)  # Зеленый в BGR
#         elif box_info['yellow_ratio'] > 0.2:
#             color = (0, 255, 255)  # Желтый в BGR
#         elif box_info['brown_ratio'] > 0.2:
#             color = (0, 0, 255)  # Коричневый в BGR
#         else:
#             color = (255, 0, 0)  # Синий в BGR
#
#         # Рисуем bounding box
#         cv2.rectangle(result_image, (x1, y1), (x2, y2), color, 3)
#
#         # Подпись
#         label = f"{class_name} {confidence:.2f}"
#         label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
#
#         # Фон для текста
#         cv2.rectangle(result_image, (x1, y1 - label_size[1] - 10),
#                       (x1 + label_size[0], y1), color, -1)
#
#         # Текст
#         cv2.putText(result_image, label, (x1, y1 - 5),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
#
#         # Дополнительная информация
#         color_label = f"color:{plant_ratio:.0%}"
#         cv2.putText(result_image, color_label, (x1, y2 + 20),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
#

# file_data = get_image_bytes(result_image, "JPEG", 90)
# original_name = os.path.basename(image_path)
# name_without_ext = os.path.splitext(original_name)[0]
# filename = f"detected_{name_without_ext}.jpg"
# try:
#     res_url = upload_images(file_data=file_data, filename=filename, content_type="image/jpeg")
#     print(f"Изображение загружено в Minio: {res_url}")
#     return res_url, len(detected_boxes)
# except Exception as e:
#     print("Ошибка загрузки в Minio")
#     return None, 0
