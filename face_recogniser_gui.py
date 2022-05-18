############## LIBRARY IMPORT #####################
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import face_recognition
from datetime import datetime
import time
import pickle
import webbrowser
from selenium import webdriver


############## Fetching encodings and classnames ###########
def gui_run():

    with open('classname.dat', 'rb') as f:
        classnames = pickle.load(f)

    print("Getting encodings....")
    with open('dataset_faces.dat', 'rb') as f:
        encodeknown = pickle.load(f)

    ############### marking ##################
    def markings(name):
        with open("found_faces.csv", "r+") as f:
            mydatalist = f.readlines()

            per = 0
            now = datetime.now()
            timenow = str(now).split()
            date = timenow[0]
            time1 = timenow[1].split(".")[0]
            for line in mydatalist:
                entry = line.split(",")
                if entry[0] == name and entry[1] == date:
                    per += 1
            if per == 0:
                mandata = f"\n{name},{date},{time1}"
                f.writelines(mandata)
                print("data recorded : ", mandata)

    ############# SUPPORTING FUNCTIONS ############
    cnd = True

    def cmnd():
        m.destroy()

    def ext():
        global cnd
        cnd = False
        m.destroy()

    def cononext():
        global cnd

        MsgBox = messagebox.askquestion('Exit Application', 'Sure to exit the application',
                                        icon='warning')
        if MsgBox == 'yes':

            cnd = False

    def changeOnHover(button, colorOnHover, colorOnLeave):
        # adjusting backgroung of the widget
        # background on entering widget
        button.bind("<Enter>", func=lambda e: button.config(
            background=colorOnHover))

        # background color on leving widget
        button.bind("<Leave>", func=lambda e: button.config(
            background=colorOnLeave))

    ########### Application starter confirmation window ##########

    m = Tk()
    m.title("Assessment centre")
    m.geometry("250x100")
    m.configure(bg="steel blue")
    m.minsize(height=100, width=250)
    m.maxsize(height=100, width=250)
    f = Frame(m, bg="cyan", height=150, width=200)
    f.pack()
    Label(f, bg="cyan", fg="steel blue",
          text="Welcome to Assessment Centre").pack()
    Label(f, bg="cyan", fg="red",
          text="Do you want to launch the application ?").pack()
    Button(m, fg="red", text="yes", command=cmnd, width=10).place(x=40, y=50)
    Button(m, fg="red", text="no", command=ext, width=10).place(x=150, y=50)

    m.mainloop()

    ######################### MAIN GUI WINDOW ##########################
    root = Tk()
    root.wm_attributes('-fullscreen', 'true')
    icn = PhotoImage(file="faceicon.jpg")
    root.iconphoto(False, icn)
    root.title("Assessment Centre - Face recogniser ")
    root.configure(bg="steel blue")

    # close button
    extbtn = Button(root, text="close", bg="white", fg="red",
                    command=cononext, font="Consolas 18 bold")
    extbtn.place(x=1260, y=75, height=40, width=80)

    time1 = Label(root, bg="blue", fg="white", font="Consolas 20 bold")
    ft = Frame(root, bg="light sky blue", height=200)
    ft.pack(fill="x", padx=10, pady=10)
    Label(ft, bg="blue", font="Algerian 12 bold underline",
          text="Assessment", fg="red").pack()
    Label(ft, bg="light sky blue", font="Arial 10 bold",
          fg="sky blue").pack(padx=30)
    Label(ft, bg="light sky blue", font="Cooper 12 bold",
          text="TASS-VISION", fg="white").pack(anchor="se", padx=20)

    f1 = LabelFrame(root, bg="blue")
    f1.pack(side=LEFT, padx=10, pady=10)
    l1 = Label(f1, bg="red")
    l1.pack(side=RIGHT)
    time.sleep(2)
    ############################# MAIN application logic ##############################

    cap = cv2.VideoCapture(0)
    while True:
        if cnd == False:
            root.destroy()

        sucess, img = cap.read()
        imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
        facescurframe = face_recognition.face_locations(imgs)
        encodescurframe = face_recognition.face_encodings(
            imgs, facescurframe)

        for encodeface, faceloc in zip(encodescurframe, facescurframe):
            matches = face_recognition.compare_faces(
                encodeknown, encodeface)
            facedis = face_recognition.face_distance(
                encodeknown, encodeface)

            matchindex = np.argmin(facedis)

            if matches[matchindex]:
                name = classnames[matchindex]
                print(name)

                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2),
                              (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                mandata = markings(name)

                # chromeda testlarni tabini ochish
                url = 'https://mover.uz'

                # webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(
                #     "/usr/bin/google-chrome %s"))
                # webbrowser.get('google-chrome').open_new(url)

                # driver = webdriver.Chrome(
                #     '/snap/chromium/1646/usr/lib/chromium-browser/chromedriver')
                # driver.maximize_window()

                print(name)
                # exit()
                break

            else:
                continue

        try:
            img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img1))
            l1["image"] = img
        except:
            break

        now = datetime.now()
        timenow = str(now).split()
        t = timenow[1].split(".")[0]
        time1["text"] = t

        root.update()



gui_run()
