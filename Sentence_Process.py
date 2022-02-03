import os

from Modules import SENTENCEmod
from Modules.Loggingkun import KyokoLoggingkun


def path_cutexthanshin(pathkun):
    pathkun334, extkun = os.path.splitext(os.path.basename(pathkun))
    return pathkun334
class Sentence_Process:
    def __init__(self,filename,loggingobj:KyokoLoggingkun,endtime,voicefile):
        self.filename=filename
        self.loggingobj=loggingobj
        self.path_ONLY = path_cutexthanshin(filename)
        self.endtime=endtime
        self.voicefile=voicefile
        self.Instance_sentence=None
    def process(self):
        self.loggingobj.normalout("<< SENTENCE >>")
        subjectCSV = './SENTENCE/csv/Asubject.csv'
        emoDic = './SENTENCE/csv/EmoWorddic.csv'
        if not os.path.exists("./SENTENCE/csv/"):
            os.makedirs("./SENTENCE/csv/")
        if not os.path.exists("./SENTENCE/split_temp/"):
            os.makedirs("./SENTENCE/split_temp/")
        self.loggingobj.normalout("Creating Instance_sentence")
        self.Instance_sentence = SENTENCEmod.Main_process(self.voicefile, self.path_ONLY, self.endtime, subjectCSV, emoDic)
        self.Instance_sentence.Info_audio()
        self.Instance_sentence.Normalize_audio()
        self.loggingobj.normalout("Normalized audio")

        starts_lengths = self.Instance_sentence.Cut_silence_detail()
        self.Instance_sentence.set_maxlskun(len(starts_lengths))
        text = self.Instance_sentence.Cut_by_silence_S()
        self.loggingobj.normalout(text)
        self.loggingobj.debugout('end')
        self.loggingobj.debugout('0s : {}\n'.format(text))
        for count in range(len(starts_lengths)-1):
            text = self.Instance_sentence.Cut_by_silence(count)
            self.loggingobj.warnout(text)
            self.loggingobj.debugout('end')
            self.loggingobj.debugout('{}s : {}\n'.format(count+1, text))
        text = self.Instance_sentence.Cut_by_silence_E()
        self.loggingobj.warnout(text)
        self.loggingobj.debugout('end')
        self.loggingobj.debugout('{}s : {}\n'.format(len(starts_lengths), text))

        # 切られた音声の位置（秒数）を記録
        SENTENCEtimememo = self.Instance_sentence.Write_startendtimes()
        self.loggingobj.successout('Exported SENTENCEtimememo')
        # 切られた音声から文字起こしされた文章を記録
        textslist = self.Instance_sentence.Write_texts()
        self.loggingobj.successout('exported textslist')

        #-------------------- Emotion dictionary part --------------------
        for count in range(len(starts_lengths)+1):
            #print('='*30)
            self.loggingobj.debugout('==============================\n')
            symbols, sentence, tokens = self.Instance_sentence.EmoRecognize(count)
            #print(sentence,'\n',tokens,'\nsymbols :',symbols)
            self.loggingobj.debugout('{}\n{}\n{}'.format(sentence, tokens, symbols))
            SYMBOLs = self.Instance_sentence.EmoChange(symbols)
            #print('SYMBOLs :', SYMBOLs)
            self.loggingobj.debugout('SYMBOLs : {}\n'.format(SYMBOLs))
            emoscount_list = self.Instance_sentence.CountEmo(SYMBOLs)
            #print('emoscount_list :', emoscount_list)
            self.loggingobj.debugout('emoscount_list : {}\n'.format(emoscount_list))
        #print('='*30)
        self.loggingobj.debugout('==============================\n')
        SENTENCEemomemo = self.Instance_sentence.Write_emos()
        self.loggingobj.successout('Exported SENTENCEemomemo')

        return SENTENCEemomemo, SENTENCEtimememo, textslist
