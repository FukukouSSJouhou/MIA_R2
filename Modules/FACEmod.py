# angry, happy, neutral, sad, surprise
# self.facepoint, timeemos
import os
import shutil
import glob
import numpy as np
import cv2
from keras.models import load_model
from keras.preprocessing import image

import math

from Modules.Loggingkun import KyokoLoggingkun


class Main_process:
    def __init__(self, video_path, pertime, video_path_ONLY, endtime,loggingobj:KyokoLoggingkun):
        self.video_path=video_path
        self.pertime=pertime
        self.video_path_ONLY=video_path_ONLY
        self.endtime = endtime
        self.loggingobj=loggingobj

        model_path = './FACE/models/5face_emotions_100ep.hdf5'
        self.emotions_XCEPTION = load_model(model_path, compile=False)

        self.timeemos=[]

        # 動画画像保存フォルダを作成
        self.imgDIR_NAME = './FACE/temp_img/img_'+self.video_path_ONLY
        if not os.path.exists(self.imgDIR_NAME):
            os.mkdir(self.imgDIR_NAME)

        if not os.path.exists('./FACE/facepointmemo/'):
            os.makedirs('./FACE/facepointmemo/')

        if not os.path.exists('./FACE/emomemo/'):
            os.makedirs('./FACE/emomemo/')

    def detect_emotion(self, index):
        try:
            face_path = self.imgDIR_NAME+'/sec'+str(index)+'.jpg'
            img_detecting = image.load_img(face_path, grayscale=True , target_size=(48, 48))
            img_array = image.img_to_array(img_detecting)
            pImg = np.expand_dims(img_array, axis=0) / 255
            prediction = self.emotions_XCEPTION.predict(pImg)[0]

            emos=[]
            for predict_i in range(len(prediction)):
                emos.append(prediction[predict_i])
            self.timeemos.append(emos)

        except FileNotFoundError:# エラーが起きた時→指定した秒数の画像が無かった時
            emos=[0,0,0,0,0]
            self.timeemos.append(emos)

        return emos

    def Write_to_textfile(self):
        # 感情値保存
        txtfile = './FACE/emomemo/'+self.video_path_ONLY+'.txt'
        f = open(txtfile, 'w')
        for a in range(len(self.timeemos)):
            for b in range(len(self.timeemos[a])):
                f.write(str(self.timeemos[a][b]))
                if b != len(self.timeemos[a])-1:
                    f.write(',')
            if a != len(self.timeemos)-1:
                f.write('\n')
        f.close()

        return txtfile


    def save_allsec_img(self):
        # 動画を取得
        #print(self.video_path,"-"*20)
        capture = cv2.VideoCapture(self.video_path)
        fps = capture.get(cv2.CAP_PROP_FPS)
        self.loggingobj.normalout(fps)

        getsec=0
        self.facepoint=[]

        # 顔を認識するためのカスケードファイルを読み込む
        cascade_path='./FACE/models/haarcascade_frontalface_default.xml'
        cascade=cv2.CascadeClassifier(cascade_path)

        self.hantei=0# target画像の処理を行ったかの判定変数

        # 各秒数の画像を処理
        self.loggingobj.normalout(math.floor(self.endtime))
        while getsec <= math.floor(self.endtime):
            # set the time
            capture.set(cv2.CAP_PROP_POS_FRAMES, round(fps*getsec))
            _, frame = capture.read()

            # execute the face detection model
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            self.front_face_list=cascade.detectMultiScale(gray)
            self.loggingobj.debugout("{} {}".format(getsec,self.front_face_list))
            self.i=0
            if len(self.front_face_list) == 0:
                self.facepoint.append([0,0,0,0])
            else:
                for (x,y,w,h) in self.front_face_list:
                    # save pictures of detected faces as jpg files
                    self.save_path = self.imgDIR_NAME+'/temp'+str(self.i)+'.jpg'
                    self.img = frame[y : y+h, x: x+w]
                    cv2.imwrite(self.save_path, self.img)
                    self.i+=1

                # target画像がまだなければ選択させるメソッドを実行する
                # target画像があれば、類似度の算出に移る
                if os.path.exists(self.imgDIR_NAME+'/target.jpg'):
                    # target画像の処理がまだであれば実行
                    if self.hantei==0:
                        # target画像の処理
                        target_img_path = self.imgDIR_NAME+'/target.jpg'
                        # target画像　グレースケール読み出し
                        target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
                        # target画像を200x200にリサイズ
                        self.target_img = cv2.resize(target_img, (200,200))

                    # 類似度の算出
                    self.similarity()
                    #print('もっとも類似度が高い画像は、',self.imgDIR_NAME+'/temp'+str(self.most_similar_index)+'.jpg')
                    # 類似度が高い方をその秒数代表写真として（コピー&）リネーム保存
                    old = self.imgDIR_NAME+'/temp'+str(self.most_similar_index)+'.jpg'
                    new = self.imgDIR_NAME+'/sec'+str(getsec)+'.jpg'
                    shutil.copy(old, new)

                    # もっとも類似度が高い画像の位置を記録
                    f_to_list = self.front_face_list[self.most_similar_index].tolist()
                    self.facepoint.append(f_to_list)

            getsec+=self.pertime

        # temp画像の削除
        temp_imgs = glob.glob(self.imgDIR_NAME+'/temp*.jpg')
        for temp_img in temp_imgs:
            os.remove(temp_img)

        # target画像の削除
        os.remove(self.imgDIR_NAME+'/target.jpg')
        # 顔の位置保存
        txtfile2 = './FACE/facepointmemo/'+self.video_path_ONLY+'.txt'
        f = open(txtfile2, 'w')
        for a in range(len(self.facepoint)):
            for b in range(len(self.facepoint[a])):
                f.write(str(self.facepoint[a][b]))
                if b != len(self.facepoint[a])-1:
                    f.write(',')
            if a != len(self.facepoint)-1:
                f.write('\n')
        f.close()

        capture.release()
        self.loggingobj.successout("Released capture")

        return txtfile2
    #---------------------------------------------------------
    # 類似度の算出
    def similarity(self):
        self.hantei=1# 類似度の判定を実行したため変数を1に変更

        #img_size = (200, 200)

        # BFMatcherオブジェクトの生成
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        # 特徴点を検出
        detector = cv2.AKAZE_create()
        #detector = cv2.ORB_create()
        (target_kp, target_des) = detector.detectAndCompute(self.target_img, None)
        #print('TARGET_FILE :', )

        similarity_list=[]
        for j in range(self.i):
            # 比較対象の写真の特徴点を検出
            comparing_img_path = self.imgDIR_NAME+'/temp'+str(j)+'.jpg'
            try:
                comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
                comparing_img = cv2.resize(comparing_img, (200,200))
                (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)

                # BFMatcherで総当たりマッチングを行う
                matches = bf.match(target_des, comparing_des)
                #特徴量の距離を出し、平均を取る
                dist = [m.distance for m in matches]
                ret_simi = sum(dist) / len(dist)

            except cv2.error:
                # cv2がエラーを吐いた場合の処理
                ret_simi = 100000

            self.loggingobj.debugout("{} {}".format(comparing_img_path, ret_simi))
            similarity_list.append(ret_simi)

        # similarity_list内で一番低い値のインデックスを取得
        self.most_similar_index = similarity_list.index(min(similarity_list))
