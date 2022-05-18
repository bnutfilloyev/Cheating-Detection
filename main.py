from multiprocessing import Process
from example import another_big
from audio import big_function
# from face_recogniser_gui import gui_run
import time
from hand_tracking_min import hand_big

#Multithreading qilingan
if __name__ == "__main__":
    # p1 = Process(target=gui_run)
    # p1.start()
    # time.sleep(20)
    # p1.terminate()
    Process(target=another_big).start()
    Process(target=big_function).start()
    # Process(target=hand_big).start()
    


