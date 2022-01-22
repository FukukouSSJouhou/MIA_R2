import os
import sys


class Face_Process():
    def __init__(self,filename,timedouga,logging_func):
        self.filename=filename
        self.timedouga=timedouga
        self.logging_func=logging_func
    def process(self):
        self.logging_func("<< FACE >>")
        if not os.path.exists(self.filename):
            self.logging_func("404 NOT FOUND")
        self.logging_func("input file name : " + self.filename)
        self.logging_func("Processing movie file :" + self.filename)
        