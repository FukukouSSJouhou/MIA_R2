import os
import subprocess
import sys
import wave
import cv2

def path_cutext(pathkun):
    pathkun22, extkun = os.path.splitext(os.path.basename(pathkun))
    return pathkun22
class Face_Process():
    def __init__(self,filename,timedouga,logging_func):
        self.voicefile = None
        self.imgDIR_NAME = None
        self.endtime = None
        self.filename=filename
        self.timedouga=timedouga
        self.logging_func=logging_func
        self.path_ONLY=path_cutext(self.filename)
    def process(self):
        self.logging_func("<< FACE >>")
        if not os.path.exists(self.filename):
            self.logging_func("404 NOT FOUND")
        self.logging_func("input file name : " + self.filename)
        self.logging_func("Processing movie file :" + self.filename)
        self.Make_audio()
        self.logging_func("Generated Wav File.")
        self.endtime=self.get_playtime()
        self.logging_func("The length of the video / audio file has been confirmed: {}".format(self.endtime))
        self.target_img_select()

    def Make_audio(self):
        dir="./_audio/"
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.voicefile = dir + self.path_ONLY + ".wav"
        resp=subprocess.check_output(["ffmpeg","-y","-i",self.filename,self.voicefile],shell=False)
    def get_playtime(self):
        with wave.open(self.voicefile,"rb") as wr:
            fr=wr.getframerate()
            fn=wr.getnframes()
            return 1.0 * fn / fr
    def target_img_select(self):
        self.imgDIR_NAME = './FACE/temp_img/img_' + self.path_ONLY
        if not os.path.exists(self.imgDIR_NAME):
            os.makedirs(self.imgDIR_NAME)
        self.logging_func(self.filename)
        capture=cv2.VideoCapture(self.filename)
        fps = capture.get(cv2.CAP_PROP_FPS)
        print('fps :',fps);print('frame :',capture.get(cv2.CAP_PROP_FRAME_COUNT))

        #self.endtime = capture.get(cv2.CAP_PROP_FRAME_COUNT) / fps
        print('endtime :',self.endtime)
        getsec = 0
        cascade_path = './FACE/models/haarcascade_frontalface_default.xml'