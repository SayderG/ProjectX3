import cv2

# захватывать кадры из видео

cap = cv2.VideoCapture('src/Dron.mp4')

# Обученные классификаторы XML описывают некоторые особенности некоторого объекта, который мы хотим обнаружить

car_cascade = cv2.CascadeClassifier('models/yolo/cars.xml')

# цикл запускается, если захват был инициализирован.

while True:

    # читает кадры из видео

    ret, frames = cap.read()

    # конвертировать в оттенки серого каждого кадра

    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

    # Обнаруживает автомобили разных размеров на входном изображении

    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    # Нарисовать прямоугольник в каждом авто

    for (x, y, w, h) in cars:
        cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Отображать кадры в окне

    cv2.imshow('video2', frames)

    # Дождаться остановки клавиши Esc

    if cv2.waitKey(33) == 27:
        break

# Отменить выделение любого связанного использования памяти
cv2.destroyAllWindows()
