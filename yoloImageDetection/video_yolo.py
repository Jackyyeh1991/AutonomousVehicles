import cv2
import numpy as np
from threading import Thread
import time

with open("yolov3.txt", 'r') as f:
    classes = [line.strip() for line in f.readlines()]
# print(classes)

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

signflag = False

def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def stop():
    print("stop the car")

def start():
    print("start the car")

def checkifStopsign(image, classes, net):
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])


    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    print("--------------------------")
    # time.sleep(10)
    for i in indices:
        if classes[class_ids[int(i)]] == "stop sign":
            global signflag 
            signflag = True
            stop()
            time.sleep(5)
            run()
            return 
    return
            # stop()
            # time.sleep(10)
            # start()
            # return True
    # print("false")
    # return False



if __name__=="__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("We can not load Webcam")

    while True:

        ret, original_frame = cap.read()
        frame = cv2.resize(original_frame, (160, 120))
        # if sightDebug:
        #     cv2.imshow("Resized Frame", frame)


        # ret, image = cap.read()
        # cv2.imshow("web cam input", frame)
        # if cv2.waitKey(25) & 0xFF == ord("q"):
        #     cv2.destroyAllWindows()
        #     break

        print("start")
        print("signflag: ", signflag)
        Thread(target=checkifStopsign, args=(original_frame, classes, net)).start()
        # checkifStopsign(original_frame, classes,net)
        print("signflag: ", signflag)
        if (signflag):
            stop()
            time.sleep(5)
            start()
            signflag = False
        for _ in range(10):
            time.sleep(0.1)
            print("1")
    cap.release()