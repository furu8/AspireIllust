import glob as gb
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import os

class Face:

    def __init__(self, user_record):
        # UserRecord
        self.ur = user_record
        # animeface
        self.cascade = cv2.CascadeClassifier('../info/feature_animeface/lbpcascade_animeface.xml')

    def triming_face(self, path):
        # user情報取得
        df = self.ur.get_user_record(path)
        user_id_list = df['user_id'].values
        save_path = '../data/pixiv/interim/face/'

        for user_id in user_id_list:
            # イラストレータごとのパスを指定
            illustrator_path = '../data/pixiv/row/'+str(user_id)+'/*'
            illust_list = gb.glob(illustrator_path)

            # 顔抽出
            for illust in illust_list:
                img = cv2.imread(illust, cv2.IMREAD_COLOR) # デフォルトカラー読み込み
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # グレースケール化
                gray_img = cv2.equalizeHist(gray_img) # ヒストグラム平均化（見やすくなる）

                face_list = self.cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
                print(illust)
                file_name = illust.split('/')[-1].split('.')
                
                if len(face_list) > 0:
                    for face in face_list:
                        x = face[0]
                        y = face[1]
                        w = face[2]
                        h = face[3]
                    
                        face_img = img[y:y+h, x:x+w]
                        # ユーザのディレクトリがなければ作成
                        user_path = save_path + '/' +str(user_id)
                        if not os.path.exists(user_path):
                            os.mkdir(user_path)

                        cv2.imwrite(user_path + file_name[0] + '.png', face_img)
                


    def get_face_illust(self):
        pass
