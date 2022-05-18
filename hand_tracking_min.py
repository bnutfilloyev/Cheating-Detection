import cv2
import mediapipe as mp
import time
from datetime import datetime

def hand_big():
    #################################
    frameWidth = 640
    frameHeight = 480
    size = (frameWidth, frameHeight)
    #################################

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('videos/output.avi', fourcc, 20.0, size)

    cap = cv2.VideoCapture(1)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    pTime = 0

    while 1:
        now = datetime.now()
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        time_text = f"{now.hour}:{now.minute}:{now.second}"
        cv2.putText(img, time_text, (490, 470), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 255, 255), 4)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    # cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        if results.multi_handedness == None or len(results.multi_handedness) == 1:
            cv2.putText(img, 'Warning', (250, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0, 0, 255), 4)
            cv2.putText(img, 'Put your hands on the desk!', (50, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0, 0, 255), 4)
            out.write(img)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f"FPS: {str(int(fps))}", (10, 470), cv2.FONT_HERSHEY_PLAIN,
                    2, (255, 255, 255), 2)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
