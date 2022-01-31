import os

from Modules import SENTENCEmod


def path_cutexthanshin(pathkun):
    pathkun334, extkun = os.path.splitext(os.path.basename(pathkun))
    return pathkun334
class Sentence_Process:
    def __init__(self,filename,logging_func,endtime,voicefile):
        self.filename=filename
        self.logging_func=logging_func
        self.path_ONLY = path_cutexthanshin(filename)
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
        self.logging_func("Creating Instance_sentence")
        Instance_sentence = SENTENCEmod.Main_process(self.voicefile, self.path_ONLY, self.endtime, subjectCSV, emoDic)
        Instance_sentence.Info_audio()
        Instance_sentence.Normalize_audio()
        self.logging_func("Normalized audio")

        starts_lengths = Instance_sentence.Cut_silence_detail()

        text = Instance_sentence.Cut_by_silence_S()
        self.logging_func(text)
        for count in range(len(starts_lengths)-1):
            text = Instance_sentence.Cut_by_silence(count)
            self.logging_func(text)
        text = Instance_sentence.Cut_by_silence_E()
        self.logging_func(text)

        print(text)
        self.logging_func('end')
        self.logging_func('0s : {}\n'.format(text))
        for count in range(len(starts_lengths)-1):
            text = Instance_sentence.Cut_by_silence(count)
            self.logging_func(text)
            self.logging_func('end')
            self.logging_func('{}s : {}\n'.format(count+1, text))
        text = Instance_sentence.Cut_by_silence_E()
        self.logging_func(text)
        self.logging_func('end')
        self.logging_func('{}s : {}\n'.format(len(starts_lengths), text))

        # 切られた音声の位置（秒数）を記録
        SENTENCEtimememo = Instance_sentence.Write_startendtimes()
        self.logging_func('\033[34m' + 'Exported SENTENCEtimememo' +'\033[0m' )
        # 切られた音声から文字起こしされた文章を記録
        textslist = Instance_sentence.Write_texts()
        self.logging_func('exported textslist')

        #-------------------- Emotion dictionary part --------------------
        for count in range(len(starts_lengths)+1):
            print('='*30)
            self.logging_func('==============================\n')
            symbols, sentence, tokens = Instance_sentence.EmoRecognize(count)
            print(sentence,'\n',tokens,'\nsymbols :',symbols)
            self.logging_func('{}\n{}\n{}'.format(sentence, tokens, symbols))
            SYMBOLs = Instance_sentence.EmoChange(symbols)
            print('SYMBOLs :', SYMBOLs)
            self.logging_func('SYMBOLs : {}\n'.format(SYMBOLs))
            emoscount_list = Instance_sentence.CountEmo(SYMBOLs)
            print('emoscount_list :', emoscount_list)
            self.logging_func('emoscount_list : {}\n'.format(emoscount_list))
        print('='*30)
        self.logging_func('==============================\n')
        SENTENCEemomemo = Instance_sentence.Write_emos()
        self.logging_func('SENTENCEemomemoが出力されました\n')

        return SENTENCEemomemo, SENTENCEtimememo, textslist
