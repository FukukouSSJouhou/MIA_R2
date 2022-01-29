import subprocess
import os
import speech_recognition as sr
import pandas as pd
from janome.tokenizer import Tokenizer
# ~subject.csv "Word","Katakana","Emotion"print
# Example.csv "Emotion", "Symbol", "Emo5Ryo"
from KyokoWT.KyokoWT.coreapis import KyokoWTGoogle
class Main_process:
    def __init__(self, voicefile, onlyfile, endtime, subjectCSV, emoDic):
        self.voicefile = voicefile
        self.onlyfile = onlyfile
        self.endtime = endtime

        self.starts_ends_list=[]
        self.textslist=[]
        #=========== Emotion dictionary part ==============
        subjectData = pd.read_csv(subjectCSV)# csvファイルの要素をDataframeで取得
        self.keywords = subjectData["Word"]# インデックスで各値取得可能
        self.symbols_BASE = subjectData["Emotion"]

        example = pd.read_csv('./SENTENCE/csv/Example.csv')
        self.symbolEXA = example["Symbol"]# 「安」「楽」「親」など細かい感情値
        self.emo5 = example["Emo5"]# 「平」「怒」「幸」「悲」「驚」の5つに分けなおした感情値

        self.tokenizer = Tokenizer(emoDic, udic_type="simpledic", udic_enc="utf8")

        self.allsentences_emos_list=[]

    def Info_audio(self):
        cmd_getinfo = ['ffmpeg','-i',self.voicefile,'-vn','-af','volumedetect','-f','null','-']
        Info = subprocess.run(cmd_getinfo, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Info_str = str(Info)
        self.mean_vol = float(Info_str[Info_str.find('mean_volume: ')+len('mean_volume: '):].split(' ')[0])
        self.max_vol = float(Info_str[Info_str.find('max_volume: ')+len('max_volume: '):].split(' ')[0])
        #print(self.mean_vol, self.max_vol)
        self.silence_vol = self.mean_vol - abs(abs(self.mean_vol)-abs(self.max_vol))
        #print(self.silence_vol)

    def Normalize_audio(self):
        cmd_normalize = ['ffmpeg','-y','-i',self.voicefile,'-af','volume='+str(self.max_vol*-1)+'dB', './SENTENCE/split_temp/normalized.wav']
        # '-y'で警告なしに上書き保存する
        subprocess.run(cmd_normalize, shell=False)

    def Cut_silence_detail(self, sillen=0.4):
        # ffmpeg -y -i ./SENTENCE/split_temp/normalized.wav -af silencedetect=noise=-39.0dB:d=0.4 -f null -
        cmd_cut_silence = ['ffmpeg','-y','-i','./SENTENCE/split_temp/normalized.wav','-af','silencedetect=noise={}dB:d={}'.format(self.mean_vol, sillen),'-f','null','-']
        silence_Info = subprocess.run(cmd_cut_silence, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print(silence_Info)
        lines = str(silence_Info).split('\\r\\n')

        time_list=[]
        for line in lines:
            if "silencedetect" in line:
                words = line.split(" ")
                #print(words)
                for i in range(len(words)):
                    if "silence_start" in words[i]:
                        #time_list.append(float(words[i+1]) + 0.5)
                        time_list.append(float(words[i+1]))
                    #if "silence_end" in words[i]:
                    #    time_list.append(float(words[i+1]))
                    if "silence_duration" in words[i]:
                        time_list.append(float(words[i+1]))
        self.starts_lengths = list(zip(*[iter(time_list)]*2))
        #print(self.starts_ends)

        return self.starts_lengths

    def Cut_by_silence_S(self):
        starttime_S = 0; endtime_S = self.starts_lengths[0][0]

        cmd_output_S = ['ffmpeg','-y','-i','./SENTENCE/split_temp/normalized.wav',
                        '-ss',str(starttime_S),
                        '-t',str(endtime_S+0.5),
                        './SENTENCE/split_temp/temp.wav']# './SENTENCE/split_temp/'+str(0).zfill(4)+'.wav'
        subprocess.run(cmd_output_S, shell=False)
        self.starts_ends_list.append([starttime_S, endtime_S])

        text = self.SpeechRecognition()
        self.textslist.append(text)

        return text

    def Cut_by_silence(self, count):
        splitfile = './SENTENCE/split_temp/'+str(count+1).zfill(4)+'.wav'
        starttime = self.starts_lengths[count][0]+self.starts_lengths[count][1]; endtime = self.starts_lengths[count+1][0]

        cmd_output = ['ffmpeg','-y','-i','./SENTENCE/split_temp/normalized.wav',
                      '-ss',str(starttime-0.3),
                      '-t',str(endtime-starttime+0.5),
                      './SENTENCE/split_temp/temp.wav']# splitfile
        subprocess.run(cmd_output, shell=False)
        self.starts_ends_list.append([starttime, endtime])

        text = self.SpeechRecognition()
        self.textslist.append(text)

        return text #[starttime, endtime]

    def Cut_by_silence_E(self):
        starttime_E = self.starts_lengths[len(self.starts_lengths)-1][0]+self.starts_lengths[len(self.starts_lengths)-1][1]; #endtime_E = self.endtime

        cmd_output_E = ['ffmpeg','-y','-i','./SENTENCE/split_temp/normalized.wav',
                        '-ss',str(starttime_E-0.3),
                        '-t',str(self.endtime-starttime_E+0.5),
                        './SENTENCE/split_temp/temp.wav']# './SENTENCE/split_temp/'+str(len(self.starts_lengths)).zfill(4)+'.wav'
        subprocess.run(cmd_output_E, shell=False)
        self.starts_ends_list.append([starttime_E, self.endtime])

        text = self.SpeechRecognition()
        self.textslist.append(text)

        return text #[starttime_E, self.endtime]

    def SpeechRecognition(self):
        try:
            k=KyokoWTGoogle()
            text=k.gettext('./SENTENCE/split_temp/temp.wav')
        except Exception as e:
            #print('========== ERROR ==========')
            text = '<empty>'
            print("type:" + str(type(e)))
            print('args:' + str(e.args))
            print('message:' + e.message)
        return text

    def Write_startendtimes(self):
        timefile='./SENTENCE/times/'+self.onlyfile+'_times.txt'
        f = open(timefile, 'w')

        for i in range(len(self.starts_ends_list)):
            f.write('{0}~{1}'.format(self.starts_ends_list[i][0], self.starts_ends_list[i][1]))
            if i != len(self.starts_ends_list)-1:
                f.write('\n')
        f.close()

        return timefile

    def Write_texts(self):
        textfile='./SENTENCE/texts/'+self.onlyfile+'.txt'
        f = open(textfile, 'w')

        for i in range(len(self.textslist)):
            f.write(self.textslist[i])
            if i != len(self.textslist)-1:
                f.write('\n')
        f.close()

        return textfile

#======================================= Emotion dictionary part ========================================
    def EmoRecognize(self, count):
        sen = self.textslist[count]
        symbols=[]
        tokens=[]
        #print("=============================================")
        #print(sen)
        for token in self.tokenizer.tokenize(sen):# 文章を分解し、一般系にして各単語をリストに格納
            tokens.append(token.base_form)
        #print(tokens)
        for i in range(len(tokens)):# 切って正規化した各単語を取得する
            contentKeywordIndexs=[]
            for j in range(len(self.keywords)):# キーワードを１つずつ取得
                if self.keywords[j] in tokens[i]:# キーワードを含むか判定
                    contentKeywordIndexs.append(j)
                    #print(self.keywords[j])
                    #print("jだよ",j)
            #print("contentKeywordIndexsだよ",contentKeywordIndexs)
            temp=[]# 一時リスト
            if contentKeywordIndexs != []:# contentKeywordIndexsリストが空じゃないとき実行
                for a_index in contentKeywordIndexs:# contentKeywordIndexsリストに含まれる単語の長さを書き出す
                    temp.append(len(self.keywords[a_index]))
                    #print("length",len(self.keywords[a_index]))
                maxIndex = temp.index(max(temp))# 最長文字列のインデックス取得
                #print(maxIndex)
                #print("contentKeywordIndexs[maxIndex] : ",contentKeywordIndexs[maxIndex])
                symbols.append(self.symbols_BASE[contentKeywordIndexs[maxIndex]])# 最長単語の細感情値格納
                if i < len(tokens)-1:# 文章最後の単語のときは実行しない
                    if tokens[i+1] == 'ない':# 単語tokens[i]の後ろの単語が「ない」だったら追加した要素削除
                        symbols.remove(self.symbols_BASE[contentKeywordIndexs[maxIndex]])
        #print(symbols)

        return symbols, sen, tokens

    def EmoChange(self, symbols):
        SYMBOLs=[]
        for i in range(len(symbols)):
            symbol_list = list(symbols[i])
            for j in range(len(symbol_list)):
                for k in range(len(self.symbolEXA)):
                    # 5種類に絞った感情に変換
                    if symbol_list[j] == self.symbolEXA[k]:
                        SYMBOLs.append(self.emo5[k])

        return SYMBOLs

    def CountEmo(self, SYMBOLs):
        emos = ['怒','幸','平','悲','驚']
        emoscount_list=[]
        temp=''
        for word in SYMBOLs:
            temp += word
        templist = list(temp)
        for emo_index in range(len(emos)):
            emocount = templist.count(emos[emo_index])
            emoscount_list.append(emocount)
        self.allsentences_emos_list.append(emoscount_list)

        return emoscount_list

    def Write_emos(self):
        #print(self.allsentences_emos_list)
        outfile = './SENTENCE/emomemo/'+self.onlyfile+'.txt'
        f = open(outfile, 'w')
        for i in range(len(self.allsentences_emos_list)):
            for j in range(len(self.allsentences_emos_list[i])):
                f.write(str(self.allsentences_emos_list[i][j]))
                if j != len(self.allsentences_emos_list[i])-1:
                    f.write(',')
            if i != len(self.allsentences_emos_list)-1:
                f.write('\n')
        f.close()

        return outfile
