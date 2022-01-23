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
from PySide2 import QtCore, QtGui

from Modules import FACEmod


def path_cutext(pathkun):
    pathkun22, extkun = os.path.splitext(os.path.basename(pathkun))
    return pathkun22


class Face_Process():
    def __init__(self, filename, timedouga, logging_func):
        self.hantei = None
        self.voicefile = None
        self.imgDIR_NAME = None
        self.endtime = None
        self.filename = filename
        self.pertime = int(timedouga)
        self.logging_func = logging_func
        self.path_ONLY = path_cutext(self.filename)

    def process(self):
        self.logging_func("<< FACE >>")
        if not os.path.exists(self.filename):
            self.logging_func("404 NOT FOUND")
        self.logging_func("input file name : " + self.filename)
        self.logging_func("Processing movie file :" + self.filename)
        self.Make_audio()
        self.logging_func("Generated Wav File.")
        self.endtime = self.get_playtime()
        self.logging_func("The length of the video / audio file has been confirmed: {}".format(self.endtime))
        self.target_img_select()
        self.logging_func("Saved Target Picture..")
        Instance_face = FACEmod.Main_process(self.filename,self.pertime,self.path_ONLY,self.endtime,self.logging_func)
        self.logging_func("Creating Instance_face...")
        FACEpointmemo = Instance_face.save_allsec_img()
        self.logging_func("Saved all images per {}".format(self.pertime))
        self.logging_func("Outputed Facepointmemo!")
        for index in range(math.floor(self.endtime)+1):
            peremos=Instance_face.detect_emotion(index)
            self.logging_func("{} : {}".format(index,peremos))
        FACEemomemo=Instance_face.Write_to_textfile()
        self.logging_func("Exported Faceemomemo!")
        return FACEemomemo, FACEpointmemo
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
        self.logging_func(self.filename)
        capture = cv2.VideoCapture(self.filename)
        fps = capture.get(cv2.CAP_PROP_FPS)
        print('fps :', fps);
        print('frame :', capture.get(cv2.CAP_PROP_FRAME_COUNT))

        # self.endtime = capture.get(cv2.CAP_PROP_FRAME_COUNT) / fps
        print('endtime :', self.endtime)
        getsec = 0
        cascade_path = './FACE/models/haarcascade_frontalface_default.xml'
        cascade = cv2.CascadeClassifier(cascade_path)
        self.hantei = 0
        while getsec <= math.floor(self.endtime):
            print(getsec)
            if not os.path.exists(self.imgDIR_NAME + '/target.jpg'):

                # set the time
                capture.set(cv2.CAP_PROP_POS_FRAMES, round(fps * getsec))
                _, frame = capture.read()

                # execute the face detection model
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.front_face_list = cascade.detectMultiScale(gray)
                print(getsec, self.front_face_list)
                # print(type(self.front_face_list))

                # self.temp_save_imgpaths=[]
                self.i = 0
                if len(self.front_face_list) == 0:
                    # self.facepoint.append([0,0,0,0])
                    continue
                else:
                    for (x, y, w, h) in self.front_face_list:
                        # save pictures of detected faces as jpg files
                        self.save_path = self.imgDIR_NAME + '/temp' + str(self.i) + '.jpg'
                        self.img = frame[y: y + h, x: x + w]
                        cv2.imwrite(self.save_path, self.img)
                        # self.temp_save_imgpaths.append(self.save_path)
                        # print("一時停止");time.sleep(2)
                        self.i += 1
                    self.select_target_img_window()
            getsec += self.pertime
    def select_target_img_window(self):
        win_width = 10 + (120 * self.i)
        win_height = 180

        self.showwin = tk.Tk()
        self.showwin.title('Select target image')
        self.showwin.geometry('{}x{}+{}+{}'.format(win_width, win_height, int(QtGui.QGuiApplication.primaryScreen().size().width() / 2 - win_width / 2),
                                                   int(QtGui.QGuiApplication.primaryScreen().size().height() / 2 - win_height / 2)))

        # 選択用のラジオボタンを配置
        # 画像それぞれのサイズを取得してshowwinのサイズを決める
        self.rdo_var_target = tk.IntVar()
        self.rdo_var_target.set(self.i + 1)
        rdo_txt = []
        # self.h_w_size=[]
        # self.showwin_h, self.showwin_w=0,0
        load_img_list = []

        for j in range(self.i):
            # print(j)
            # ラジオボタンに表示するテキストをリストに追加
            rdo_txt.append('img-' + str(j + 1))
            # ラジオボタンを配置
            rdo_target_select = ttk.Radiobutton(self.showwin, variable=self.rdo_var_target, value=j + 1,
                                                text=rdo_txt[j])
            rdo_target_select.place(x=10 + 25 + (100 * j), y=120)
            # 各画像の横縦サイズを取得
            # self.img_property_ndarray = cv2.imread(self.imgDIR_NAME+'/temp'+str(self.j)+'.jpg')
            # self.h, self.w, _ = self.img_property_ndarray.shape
            # h = self.front_face_list[j][2]
            # w = self.front_face_list[j][3]
            # self.h_w_size.append([h, w])
            # self.showwin_h+=self.h
            # self.showwin_w+=self.w
            # print('sum_h :',self.showwin_h,'  sum_w :',self.showwin_w)

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
