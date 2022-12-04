import cv2


if __name__=="__main__":
    print("hihi")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("We can not load Webcam")

    while True:
        ret, frame = cap.read()
        cv2.imshow("web cam input", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break




        
    
    cap.release()