import glob as gb
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import os
from UserRecord import UserRecord

class Face:

    def __init__(self):
        # UserRecord
        self.ur = UserRecord()
        # animeface
        self.cascade = cv2.CascadeClassifier('../info/feature_animeface/lbpcascade_animeface.xml')
        # 顔画像リスト
        self.face_img_list = []

    def triming_face(self, save_path):
        using_illust_path = '../info/follow_user_account/user_account_using.json' # ユーザ情報保存先
        # user情報取得
        user_id_list = self.__get_user_id_list(using_illust_path)

        # イラストレータごと
        for user_id in user_id_list:
            # イラストレータごとのパスを指定
            illustrator_path = '../data/pixiv/row/' + str(user_id) + '/*'
            # イラストリスト
            illust_path_list = gb.glob(illustrator_path)
            # イラストごとにトリミング
            self.triming_face_from_illust(save_path, illust_path_list, user_id)

    def triming_face_from_illust(self, save_path, illust_list, user_id):
        # イラストごと
        for illust in illust_list:
            # 保存するファイル名
            save_file_name = illust.split('/')[-1].split('.')[0]
            print(save_file_name)
            # 顔抽出
            img, face_list = self.__get_face_img(illust)
            
            if len(face_list) == 0:
                continue
            # キャラごと
            for i, face in enumerate(face_list):
                x, y, w, h = face # x始点、y始点、w幅、h高さ
                face_img = img[y:y+h, x:x+w] # トリミング

                # ユーザのディレクトリがなければ作成
                user_path = save_path + str(user_id) + '/'
                self.__make_directory(user_path)

                # pngで保存
                path = user_path + save_file_name + '_' + str(i+1) + '.png'
                self.__save_illust(path, face_img)
                
    def get_face_illust(self):
        return self.face_img_list
    
    def __save_illust(self, path, face_img):
        if not os.path.exists(path): # DL済みの画像かどうか判定
            cv2.imwrite(path, face_img) # 保存
            print(path + 'をトリミングし保存しました')
            self.face_img_list.append(face_img)

    def __resize_illust(self):
        pass

    # user情報取得
    def __get_user_id_list(self, path):
        df = self.ur.get_user_record(path)
        user_id_list = df['user_id'].values
        return user_id_list

    # ディレクトリがなければ作成
    def __make_directory(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
            print('{}にディレクトリ作成'.format(path))

    # 顔抽出
    def __get_face_img(self, illust):
        img = cv2.imread(illust, cv2.IMREAD_COLOR) # デフォルトカラー読み込み
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # グレースケール化
        gray_img = cv2.equalizeHist(gray_img) # ヒストグラム平均化（見やすくなる）
        # face_list = self.cascade.detectMultiScale(gray_img, scaleFactor=1.01, minNeighbors=5, minSize=(24, 24)) # 見逃しを極力少なくパラメータ設定した場合
        face_list = self.cascade.detectMultiScale(gray_img, scaleFactor=1.09, minNeighbors=5, minSize=(24, 24)) # 誤検知を極力少なくパラメータ設定した場合
        return img, face_list

# テスト
if __name__ == "__main__":
    face = Face()
    
    # test1
    shirabi = 216403
    kantoku = 1565632
    face.triming_face_from_illust('../data/pixiv/interim/face/face_test/', ['../data/pixiv/interim/face/face_test/test_kantoku.jpg'], kantoku)
    # face.triming_face_from_illust('../data/pixiv/interim/face/face_test/', ['../data/pixiv/interim/face/face_test/test_shirabi.jpg'], shirabi)
    
    # test2
    print(face.get_face_illust())