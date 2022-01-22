import os
import subprocess
import sys


def path_cutext(pathkun):
    pathkun22, extkun = os.path.splitext(os.path.basename(pathkun))
    return pathkun22
class Face_Process():
    def __init__(self,filename,timedouga,logging_func):
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
    def Make_audio(self):
        dir="./_audio/"
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.voicefile = dir + self.path_ONLY + ".wav"
        resp=subprocess.check_output(["ffmpeg","-y","-i",self.filename,self.voicefile],shell=False)