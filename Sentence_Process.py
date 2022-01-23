import os

from Modules import SENTENCEmod


def path_cutexthanshin(pathkun):
    pathkun334, extkun = os.path.splitext(os.path.basename(pathkun))
    return pathkun334
class Sentence_Process:
    def __init__(self,filename,logging_func,endtime,voicefile):
        self.filename=filename
        self.logging_func=logging_func
        self.path_ONLY = path_cutexthanshin
        self.endtime=endtime
        self.voicefile=voicefile

    def process(self):
        self.logging_func("<< SENTENCE >>")
        subjectCSV = './SENTENCE/csv/Asubject.csv'
        emoDic = './SENTENCE/csv/EmoWorddic.csv'
        if not os.path.exists("./SENTENCE/csv/"):
            os.makedirs("./SENTENCE/csv/")
        if not os.path.exists("./SENTENCE/split_temp/"):
            os.makedirs("./SENTENCE/split_temp/")
        Instance_sentence = SENTENCEmod.Main_process(self.voicefile, self.path_ONLY, self.endtime, subjectCSV, emoDic)
        Instance_sentence.Info_audio()
        Instance_sentence.Normalize_audio()

