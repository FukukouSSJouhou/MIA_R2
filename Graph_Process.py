import os

from Modules import GRAPHmod


def path_cutext2(pathkun):
    pathkun22, extkun = os.path.splitext(os.path.basename(pathkun))
    return pathkun22
class Graph_Process:
    def __init__(self,filename,logging_func):
        self.filename=filename
        self.path_ONLY=path_cutext2(self.filename)
        self.logging_func=logging_func
    def process(self,F1,V1,S1,S2):
        self.logging_func("<< GRAPH >>")
        #Instance1_graph=GRAPHmod.NumProcess(self.path_ONLY, F1, V1, S1, S2)
        #self.logging_func("Creating Instance1_graph")
        #F_list, V_list, S_list = Instance1_graph.Getlists()
        #FVS_list = Instance1_graph.Calculate_with_VS()
        Instance2_graph = GRAPHmod.DrawGraphs(self.path_ONLY)
        self.logging_func("Creating Instance2_graph")

        savename_F = Instance2_graph.Draw(F1, 1)
        self.logging_func("Exported savename_F")
        savename_FVS=""
        return savename_F, savename_FVS
    def process(self,F1):
        self.logging_func("<< GRAPH >>")
        #Instance1_graph=GRAPHmod.NumProcess(self.path_ONLY, F1, V1, S1, S2)
        #self.logging_func("Creating Instance1_graph")
        #F_list, V_list, S_list = Instance1_graph.Getlists()
        #FVS_list = Instance1_graph.Calculate_with_VS()
        Instance2_graph = GRAPHmod.DrawGraphs(self.path_ONLY)
        savename_F = Instance2_graph.Draw(F1, 1)
        return savename_F