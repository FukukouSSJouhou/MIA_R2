import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class NumProcess:
    def Read_F(self, textfile):
        f = open(textfile, 'r'); texts = f.readlines(); f.close()
        LIST=[]
        for i in range(len(texts)):
            emolist = texts[i].rstrip('\n').split(',')
            List=[]
            for j in range(len(emolist)):
                List.append(float(emolist[j]))
            LIST.append(List)
        return LIST

    def Read_V(self, textfile):
        f = open(textfile, 'r'); texts = f.readlines(); f.close()
        every4sec_list=[]
        for i in range(len(texts)):
            emolist = texts[i].rstrip('\n').split(',')
            List=[]
            for j in range(len(emolist)):
                List.append(int(emolist[j]))
            every4sec_list.append(List)

        LIST = [[0,0,0,0,0]] * self.count
        for i in range(len(every4sec_list)):
            if i != len(every4sec_list)-1:
                for j in range(4):
                    LIST[i*4+j] = every4sec_list[i]
            else:
                for j in range(5):
                    LIST[i*4+j] = every4sec_list[i]
        return LIST

    def Read_S(self, emotext, timetext):
        LIST = [[0,0,0,0,0]] * self.count

        f = open(emotext, 'r'); emotexts = f.readlines(); f.close()
        emolist=[]
        for i in range(len(emotexts)):
            List = emotexts[i].rstrip('\n').split(',')
            list_temp=[]
            for j in range(len(List)):
                list_temp.append(int(List[j]))
            emolist.append(list_temp)

        f = open(timetext, 'r'); timetexts = f.readlines(); f.close()
        timelist=[]
        for i in range(len(timetexts)):
            List = timetexts[i].rstrip('\n').split('~')
            list_temp=[]
            for j in range(len(List)):
                list_temp.append(float(List[j]))
            timelist.append(list_temp)

        #print(emolist)
        for i in range(len(timelist)):
            #print(i)
            count = math.floor(timelist[i][0])# -1は一応
            #print(timelist[i][0],'~', timelist[i][1])
            #print('count :', count)

            while True:
                if count < timelist[i][0]:
                    count += 1
                    continue

                elif timelist[i][0] <= count <= timelist[i][1]:
                    #print(count)
                    #LIST[count] = i
                    LIST[count] = emolist[i]
                    count += 1

                elif timelist[i][1] < count:
                    break

        return LIST


    def __init__(self, path_ONLY, F1, V1, S1, S2):
        self.path_ONLY = path_ONLY
        self.FACE = self.Read_F(F1)
        self.count = len(self.FACE)# abe_speech_0_46の場合 47
        self.VOICE = self.Read_V(V1)
        self.SENTENCE = self.Read_S(S1, S2)

    def Getlists(self):
        return self.FACE, self.VOICE, self.SENTENCE

    def Calculate_with_VS(self):
        self.after_List = [0] * self.count

        for i in range(self.count):
            #F = self.FACE[i]# [0.0015841936, 0.7780537, 0.13871375, 0.08128963, 0.00035874394]
            #V = self.VOICE[i]# [0,9,39,1,8]
            #S = self.SENTENCE[i]# [0,0,0,0,0]
            list1=[]
            for j in range(5):
                F = self.FACE[i][j]
                V = self.VOICE[i][j]
                S = self.SENTENCE[i][j]

                # with VOICE data
                val_V = (100 + V)/100
                F = F * val_V
                # with SENTENCE data
                val_S = (100 + 10*S)/100
                F = F * val_S

                list1.append(F)

            list_sum = sum(list1)
            list2=[]
            for j in range(5):
                if list_sum != 0:
                    val = list1[j]/list_sum
                else:
                    val = 0
                list2.append(val)
            self.after_List[i] = list2

        return self.after_List

    def Write_after(self):
        if not os.path.exists('./MakeGraph/afteremomemo/'):
            os.makedirs('./MakeGraph/afteremomemo/')
        txtfile = './MakeGraph/afteremomemo/'+self.path_ONLY+'.txt'
        f = open(txtfile, 'w')
        for a in range(len(self.after_List)):
            for b in range(len(self.after_List[a])):
                f.write(str(self.after_List[a][b]))
                if b != len(self.after_List[a])-1:
                    f.write(',')
            if a != len(self.after_List)-1:
                f.write('\n')
        f.close()

        return txtfile

"""colors
angry:red(#ff0000)
happy:yellow(#ffff00)
neutral:black(#000000)
sad:blue(#0000ff)
surprise:lime(#00ff00)
"""
class DrawGraphs:
    def __init__(self, path_ONLY):
        self.path_ONLY = path_ONLY
        if not os.path.exists("./MakeGraph/graphs/"):
            os.makedirs("./MakeGraph/graphs/")

    def Draw(self, file, OneORThree):
        colors=["#ff0000","#ffff00","#000000","#0000ff","#00ff00"]

        f = open(file, 'r'); texts = f.readlines(); f.close()
        emolist=[]
        for i in range(len(texts)):
            LIST = texts[i].rstrip('\n').split(',')
            List=[]
            for j in range(len(LIST)):
                List.append(float(LIST[j]))
            emolist.append(List)

        ylist=[[],[],[],[],[]]
        for i in range(5):
            for j in range(len(emolist)):
                ylist[i].append(emolist[j][i])

        x = list(range(len(emolist)))
        print(x)

        # make a figure
        fig = plt.figure()
        # set ax to the figure
        ax = fig.add_subplot(1,1,1)
        # plot on axes
        if OneORThree == 1:
            linetype = '-'
            title = 'detected emotions (Face only)'
        elif OneORThree == 3:
            linetype = '--'
            title = 'detected emotions (Face & Voice & Sentence)'
        for i in range(5):
            ax.plot(x,ylist[i],linetype,c=colors[i],linewidth=1)

        # 汎用要素
        ax.grid(True)
        ax.set_xlabel('time [sec]')
        ax.set_ylabel('exist rate')
        ax.set_title(title)
        ax.legend(['angry','happy','neutral','sad','surprise'])

        # save graph image
        savename = "./MakeGraph/graphs/"+str(OneORThree)+self.path_ONLY+".png"
        plt.savefig(savename)

        # show <Warn!>If you show graph before saving it, not to be able to save graph image
        #plt.show()

        return savename
