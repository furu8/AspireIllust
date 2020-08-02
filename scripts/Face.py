import glob as gb
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import os
from UserRecord import UserRecord

class Face:

    def __init__(self, ill_path):
        # UserRecord
        self.ur = UserRecord()
        # illustrator path
        self.illustrator_account_path = ill_path
        # animeface
        self.cascade = cv2.CascadeClassifier('../info/feature_animeface/lbpcascade_animeface.xml')

    def triming_face(self, save_path):
        user_id_list = self.__get_user_id_list(self.ill_path)

        # イラストレータごと
        for user_id in user_id_list:
            # イラストレータごとのパスを指定
            illustrator_path = '../data/pixiv/row/' + str(user_id) + '/*'
            # イラストリスト
            illust_path_list = gb.glob(illustrator_path)
            # イラストごとにトリミング
            self.triming_face_from_illust(save_path, illust_path_list)

    def triming_face_from_illust(self, save_path, illust_list):
        # イラストごと
        for illust in illust_list:
            # 保存するファイル名
            save_file_name = illust.split('/')[-1].split('.')[0]
            # 顔抽出
            img = cv2.imread(illust, cv2.IMREAD_COLOR) # デフォルトカラー読み込み
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # グレースケール化
            gray_img = cv2.equalizeHist(gray_img) # ヒストグラム平均化（見やすくなる）
            face_list = self.cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
            
            if len(face_list) > 0:
                # キャラごと
                for face in face_list:
                    # x始点、y始点、w幅、h高さ
                    x, y, w, h = face
                    # トリミング
                    face_img = img[y:y+h, x:x+w]
                    # ユーザのディレクトリがなければ作成
                    user_path = save_path + str(user_id) + '/'
                    self.__make_directory(user_path)
                    # pngで保存
                    cv2.imwrite(user_path + save_file_name + '.png', face_img)
                    print(save_file_name + '.png をトリミングし保存しました')
                
    def get_face_illust(self):
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

if __name__ == "__main__":
    face = Face('../info/follow_user_account/user_account_using.json')
    face.triming_face_from_illust('../data/pixiv/interim/face/face_test', '../data/pixiv/interim/face/face_test/test_kantoku.jpg')