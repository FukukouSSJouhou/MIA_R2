
import sys
import os
import threading
from PySide2 import QtCore, QtWidgets, QtQml

from Face_Process import Face_Process
from Graph_Process import Graph_Process
from Sentence_Process import Sentence_Process


class MainWindowConnect(QtCore.QObject):
    logging_addsignal=QtCore.Signal(str)
    gengraph_dialog_errkunsignal=QtCore.Signal(str)
    show_picture_graph1=QtCore.Signal(str,str)
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

    @QtCore.Slot(str,float,bool)
    def running_syori_clicked(self,filepath2,float_byou2,sentence_checked):
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
            self.logging_addsignal.emit("Main Th!")
            self.logging_addsignal.emit("Processing pictures...")
            fp=Face_Process(self.videofilepath,self.floatbyou,self.logging_addsignal.emit)
            FACEemomemo, FACEpointmemo,endtime,voicefile =  fp.process()
            self.FACEemomemo=FACEemomemo
            self.FACEpointmemo=FACEpointmemo
            if self.sentence_enabled:
                sp=Sentence_Process(self.videofilepath,self.logging_addsignal.emit,endtime,voicefile)
                sp.process()
            self.logging_addsignal.emit("Success!")
            print('\033[34m' + 'Success!!' + '\033[0m')
            self.is_valid=True
    @QtCore.Slot()
    def genGraph_Clicked(self):
        if self.FACEemomemo is None or self.FACEpointmemo is None:
            self.gengraph_dialog_errkunsignal.emit("Err")
            return
        gp=Graph_Process(self.videofilepath,self.logging_addsignal.emit)
        graph_F =gp.process(self.FACEemomemo)
        self.show_picture_graph1.emit(graph_F,"Graph Face Only!")


