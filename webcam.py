import cv2
import time
from datetime import datetime


def takePicture(directory, cycle):
    cap = cv2.VideoCapture(0)
    capture_duration = 2  
    start_time = time.time()
    while True:
        ret, image = cap.read()
        if not ret:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elapsed_time = time.time() - start_time
        if elapsed_time >= capture_duration:
            break
    cv2.imwrite(directory, image)
    name = str(datetime.now()) + "Cycle " + str(cycle) + ".jpg"
    cv2.imwrite(f"imagedata/{name}", image)
    cap.release()
    cv2.destroyAllWindows()


