
import sys
import os
import threading
from PySide2 import QtCore, QtWidgets, QtQml

from Face_Process import Face_Process
from Graph_Process import Graph_Process
from Modules.Loggingkun import KyokoLoggingkun
from Sentence_Process import Sentence_Process


class MainWindowConnect(QtCore.QObject):
    logging_addsignal=QtCore.Signal(str)
    gengraph_dialog_errkunsignal=QtCore.Signal(str)
    show_picture_graph1=QtCore.Signal(str,str)
    logging_ansi_addsignal=QtCore.Signal(str,str)
    set_runbuttonstate=QtCore.Signal(bool)
    def __init__(self, parent=None):
        super(MainWindowConnect, self).__init__(parent)
        self.sentence_enabled = False
        self.FACEpointmemo = None
        self.FACEemomemo = None
        self.flag = 0
        self.is_valid=True
        self.instance = []
        self.videofilepath=""
        self.floatbyou=0
        self.loggingobj=KyokoLoggingkun(self.logging_print_crcode, self.logging_print_nocrcode)
    def logging_print_crcode(self,colorcode,text):
        r = int(colorcode[1:3], 16)
        g = int(colorcode[3:5], 16)
        b = int(colorcode[5:7], 16)
        print("\033[38;2;{};{};{}m{}\033[0m".format(r,g,b,text))
        self.logging_ansi_addsignal.emit(colorcode,str(text).replace("<","&lt;").replace(">","&gt;"))
    def logging_print_nocrcode(self,text):
        print(text)
        self.logging_addsignal.emit(str(text).replace("<","&lt;").replace(">","&gt;"))
    @QtCore.Slot(str,float,bool,bool)
    def running_syori_clicked(self,filepath2,float_byou2,sentence_checked,voice_checked):
        self.videofilepath=filepath2
        self.floatbyou=float_byou2
        self.sentence_enabled=sentence_checked
        self.thread1=threading.Thread(target=self.mainProgram)
        self.thread1.setDaemon(True)
        self.thread1.start()
    @QtCore.Slot(str)
    def print_stdout(selfself,strtextkun):
        print(strtextkun)
    @QtCore.Slot(str ,result='QVariant')
    def videoFilePathSet(self,furl):
        print(furl)
        return QtCore.QDir.toNativeSeparators(QtCore.QUrl(furl).toLocalFile())
    def mainProgram(self):
        if self.is_valid:
            self.is_valid=False
            self.set_runbuttonstate.emit(False)
            self.loggingobj.normalout("Main Thread!")
            self.loggingobj.normalout("Processing pictures...")
            fp=Face_Process(self.videofilepath,self.floatbyou,self.loggingobj)
            FACEemomemo, FACEpointmemo,endtime,voicefile =  fp.process()
            self.FACEemomemo=FACEemomemo
            self.FACEpointmemo=FACEpointmemo
            if self.sentence_enabled:
                self.loggingobj.normalout("Running neutral language processing🖋....")
                sp=Sentence_Process(self.videofilepath,self.loggingobj,endtime,voicefile)
                SENTENCEemomemo, SENTENCEtimememo, textslist = sp.process()
            self.loggingobj.successout("Success!")
            #print('\033[34m' + 'Success!!' + '\033[0m')
            self.set_runbuttonstate.emit(True)
            self.is_valid=True
    @QtCore.Slot()
    def genGraph_Clicked(self):
        if self.FACEemomemo is None or self.FACEpointmemo is None:
            self.gengraph_dialog_errkunsignal.emit("Err")
            return
        gp=Graph_Process(self.videofilepath,self.loggingobj)
        graph_F =gp.process(self.FACEemomemo)
        self.show_picture_graph1.emit(graph_F,"Graph Face Only!")


