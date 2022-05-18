import os
import cv2
from gaze_tracking import GazeTracking
import mediapipe as mp
import time
from datetime import date, datetime
import os

def another_big():
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    current_dir = os.getcwd()

    webcam.set(3, 1280)
    webcam.set(4, 720)


    cTime = 0
    pTime = 0

    # Draw face
    mpDraw = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
    drawSpec = mpDraw.DrawingSpec(thickness=5, circle_radius=5)
    last_saved_time = datetime.now()

    while True:
        ret, frame = webcam.read()
        if ret:
            gaze.refresh(frame)
            frame = gaze.annotated_frame()
            text = ""

            imgRGB = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            results = faceMesh.process(imgRGB)
            cheated = False


            if results.multi_face_landmarks:
                for faceLms in results.multi_face_landmarks:
                    for lm in faceLms.landmark:
                        z = int(lm.z * 1000)
                        if z < -6 or z > 20 or gaze.is_right() or gaze.is_left():
                            drawSpec = mpDraw.DrawingSpec(color=(0, 0, 255))
                            cheated = True 
                        else:
                            drawSpec = mpDraw.DrawingSpec(color=(0, 255, 0))
                    mpDraw.draw_landmarks(frame, faceLms, mpFaceMesh.FACE_CONNECTIONS, drawSpec, drawSpec)
                    

            cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

         
            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
            cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


            ### FPS
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            # FPS text
            cv2.putText(frame, f"FPS:{int(fps)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            #nechchi sekund o'tganini print qilish
            print(int((datetime.now() - last_saved_time).total_seconds()))

            cv2.imshow("Assessment Centre", frame)

            if cheated:
                # cheating_time = datetime.now().strftime("%H-%M-%S")
                # cv2.imwrite(os.path.join(f"{current_dir}/snaps/{cheating_time}.png"), frame)
                # last_saved_time = datetime.now()
            #     last_saved_time = datetime.now()
            #     cv2.imwrite("snaps/{}.jpg".format(datetime.now()), frame)
                # print("Saved snap")
                cheated = False
            if cv2.waitKey(1) == 27:
                break
        else:
            print("Empty frame")



# another_big()
