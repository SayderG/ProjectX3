import cv2
import argparse

import torch as torch

parser = argparse.ArgumentParser()
parser.add_argument('url', nargs='?', default=0)
parser.add_argument('cuda', nargs='?', default=False)


class CameraControl:
    def __init__(self, cuda: bool = False, url=0):
        self._YOLO_VERSION = "v4-tiny"
        self._MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        self._is_cuda = cuda
        self._capture = cv2.VideoCapture(url)
        self._colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        self._model = None
        self._class_list = self.load_classes()

    def build_model(self):
        net = cv2.dnn.readNet(f"models/yolo/yolo{self._YOLO_VERSION}.weights",
                              f"models/yolo/yolo{self._YOLO_VERSION}.cfg")
        if self._is_cuda:
            print("Attempty to use CUDA")
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        else:
            print("Running on CPU")
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)
        return model

    def load_classes(self):
        with open("models/classes.txt", "r") as f:
            class_list = [cname.strip() for cname in f.readlines()]
        return class_list

    def frame_check(self, frame, needed_class='car'):
        classIds, confidences, boxes = self._model.detect(frame, .2, .4)
        person_counter = 0
        for (classid, confidence, box) in zip(classIds, confidences, boxes):
            color = self._colors[int(classid) % len(self._colors)]
            class_name = self._class_list[classid]
            if class_name == needed_class and confidence > 0.3:
                person_counter += 1
                cv2.rectangle(frame, box, color, 2)
        cv2.putText(
            img=frame,
            text=f"{person_counter} машин",
            org=(frame.shape[1] - 320, 64),
            thickness=2,
            color=(200, 20, 20),
            lineType=cv2.LINE_AA,
            fontScale=1.5,
            fontFace=cv2.FONT_HERSHEY_COMPLEX
        )

    def video_detector_any(self):
        self._model = self.build_model()
        while cv2.waitKey(1) < 1:
            ret, frame = self._capture.read()
            if not ret: break
            self.frame_check(frame)
            cv2.imshow("Neuron demo", frame)

    def video_detector_v5(self):
        self._model = torch.hub.load("ultralytics/yolov5", 'custom', 'models/yolo/yolov5.pt')
        while cv2.waitKey(1) < 1:
            ret, frame = self._capture.read()
            if not ret: break
            frame = self._model(frame)
            cv2.imshow("Neuron demo", frame.render(labels=False)[0])


if __name__ == '__main__':
    args = parser.parse_args()
    CameraControl(url="src/Dron.mov", cuda=False).video_detector_v5()
