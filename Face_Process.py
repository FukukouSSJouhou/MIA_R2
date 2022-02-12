import math
import os
import shutil
import subprocess
import sys
import wave
from tkinter import Image, ttk

import cv2
import tkinter as tk

from PIL import Image, ImageTk

from Modules import FACEmod
from Modules.Loggingkun import KyokoLoggingkun


def path_cutext(pathkun):
    pathkun22, extkun = os.path.splitext(os.path.basename(pathkun))
    return pathkun22


class Face_Process():
    def __init__(self, filename, timedouga, loggingobj:KyokoLoggingkun,screen_w,screen_h):
        self.hantei = None
        self.voicefile = None
        self.imgDIR_NAME = None
        self.endtime = None
        self.screen_w=screen_w
        self.screen_h=screen_h
        self.filename = filename
        self.pertime = int(timedouga)
        self.loggingobj = loggingobj
        self.path_ONLY = path_cutext(self.filename)
    def process_onlyaudio(self):
        self.loggingobj.normalout("<< (Only Audio) >>")
        if not os.path.exists(self.filename):
            self.loggingobj.errout("404 NOT FOUND")
        self.loggingobj.normalout("input file name : " + self.filename)
        self.loggingobj.normalout("Processing movie file :" + self.filename)
        self.Make_audio()
        self.loggingobj.successout("Generated Wav File.")
        self.endtime = self.get_playtime()
        self.loggingobj.successout("The length of the video / audio file has been confirmed: {}".format(self.endtime))
        return self.endtime,self.voicefile
    def process(self):
        self.loggingobj.normalout("<< FACE >>")
        if not os.path.exists(self.filename):
            self.loggingobj.errout("404 NOT FOUND")
        self.loggingobj.normalout("input file name : " + self.filename)
        self.loggingobj.normalout("Processing movie file :" + self.filename)
        self.Make_audio()
        self.loggingobj.successout("Generated Wav File.")
        self.endtime = self.get_playtime()
        self.loggingobj.successout("The length of the video / audio file has been confirmed: {}".format(self.endtime))
        self.target_img_select()
        self.loggingobj.successout("Saved Target Picture..")
        Instance_face = FACEmod.Main_process(self.filename,self.pertime,self.path_ONLY,self.endtime,self.loggingobj)
        self.loggingobj.normalout("Creating Instance_face...")
        FACEpointmemo = Instance_face.save_allsec_img()
        self.loggingobj.successout("Saved all images per {}".format(self.pertime))
        self.loggingobj.successout("Outputed Facepointmemo!")
        for index in range(math.floor(self.endtime)+1):
            peremos=Instance_face.detect_emotion(index)
            self.loggingobj.debugout("{} : {}".format(index,peremos))
        FACEemomemo=Instance_face.Write_to_textfile()
        self.loggingobj.successout("Exported Faceemomemo!")
        return FACEemomemo, FACEpointmemo,self.endtime,self.voicefile
    def Make_audio(self):
        dir = "./_audio/"
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.voicefile = dir + self.path_ONLY + ".wav"
        resp = subprocess.check_output(["ffmpeg", "-y", "-i", self.filename, self.voicefile], shell=False)

    def get_playtime(self):
        with wave.open(self.voicefile, "rb") as wr:
            fr = wr.getframerate()
            fn = wr.getnframes()
            return 1.0 * fn / fr

    def target_img_select(self):
        self.imgDIR_NAME = './FACE/temp_img/img_' + self.path_ONLY
        if not os.path.exists(self.imgDIR_NAME):
            os.makedirs(self.imgDIR_NAME)
        self.loggingobj.debugout(self.filename)
        capture = cv2.VideoCapture(self.filename)
        fps = capture.get(cv2.CAP_PROP_FPS)
        self.loggingobj.debugout('fps : {}'.format(fps))
        self.loggingobj.debugout('frame : {}'.format(capture.get(cv2.CAP_PROP_FRAME_COUNT)))
        self.loggingobj.debugout("endtime : {}".format(self.endtime))
        getsec = 0
        cascade_path = './FACE/models/haarcascade_frontalface_default.xml'
        cascade = cv2.CascadeClassifier(cascade_path)
        self.hantei = 0
        while getsec <= math.floor(self.endtime):
            if not os.path.exists(self.imgDIR_NAME + '/target.jpg'):

                # set the time
                capture.set(cv2.CAP_PROP_POS_FRAMES, round(fps * getsec))
                _, frame = capture.read()

                # execute the face detection model
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.front_face_list = cascade.detectMultiScale(gray)
                self.loggingobj.debugout("{} {}".format(getsec, self.front_face_list))
                self.i = 0
                if len(self.front_face_list) == 0:
                    getsec += self.pertime
                    continue
                else:
                    for (x, y, w, h) in self.front_face_list:
                        # save pictures of detected faces as jpg files
                        self.save_path = self.imgDIR_NAME + '/temp' + str(self.i) + '.jpg'
                        self.img = frame[y: y + h, x: x + w]
                        cv2.imwrite(self.save_path, self.img)
                        self.i += 1
                    self.select_target_img_window()
            getsec += self.pertime
    def select_target_img_window(self):
        win_width = 10 + (120 * self.i)
        win_height = 180

        self.showwin = tk.Tk()
        self.showwin.title('Select target image')
        self.showwin.geometry('{}x{}+{}+{}'.format(win_width, win_height, int(self.screen_w / 2 - win_width / 2),
                                                   int(self.screen_h / 2 - win_height / 2)))

        # 選択用のラジオボタンを配置
        # 画像それぞれのサイズを取得してshowwinのサイズを決める
        self.rdo_var_target = tk.IntVar()
        self.rdo_var_target.set(self.i + 1)
        rdo_txt = []
        load_img_list = []

        for j in range(self.i):
            # print(j)
            # ラジオボタンに表示するテキストをリストに追加
            rdo_txt.append('img-' + str(j + 1))
            # ラジオボタンを配置
            rdo_target_select = ttk.Radiobutton(self.showwin, variable=self.rdo_var_target, value=j + 1,
                                                text=rdo_txt[j])
            rdo_target_select.place(x=10 + 25 + (100 * j), y=120)

            # jpg画像ファイルを読み込む
            pil_img = Image.open(self.imgDIR_NAME + '/temp' + str(j) + '.jpg')
            pil_img_resize = pil_img.resize(size=(100, 100))
            photo_img = ImageTk.PhotoImage(image=pil_img_resize, master=self.showwin)
            load_img_list.append(photo_img)

        # 一番最後に、target画像が無かった場合に選択するラジオボタンを配置
        rdo_target_select = ttk.Radiobutton(self.showwin, variable=self.rdo_var_target, value=self.i + 1,
                                            text='target画像がない')
        rdo_target_select.place(x=5, y=140)

        # キャンバスを作成して配置
        for j in range(self.i):
            canvas = tk.Canvas(self.showwin, width=100, height=100)
            canvas.create_image(50, 50, image=load_img_list[j])
            # canvas['bg'] = "magenta"
            canvas.place(x=10 + (110 * j), y=10)

        self.showwin.resizable(0, 0)
        self.showwin.grab_set() # モーダル化
        self.showwin.focus_set()  # フォーカスを移 # サブウィンドウをタスクバーに表示しない

        self.showwin.mainloop()
        self.showwin_close()

    def showwin_close(self):
        ##### showwinを消した時の処理 #####
        rdo_which = self.rdo_var_target.get()
        print(rdo_which)
        # 'target画像がない'を選択していない場合、処理
        if rdo_which-1 != self.i:
            old = self.imgDIR_NAME+'/temp'+str(rdo_which-1)+'.jpg'
            new = self.imgDIR_NAME+'/target.jpg'
            shutil.copy(old, new)
        else:
            return
