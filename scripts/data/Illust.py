import os
import json
import time
import pandas as pd
import cv2
import glob as gb
import matplotlib.pyplot as plt
from UserRecord import UserRecord

class Illust:

    def __init__(self, p_api, p_aapi):
        # pixiv api
        self.p_api = p_api
        self.p_aapi = p_aapi
        # UserRecord
        self.ur = UserRecord()
        # animeface
        self.cascade = cv2.CascadeClassifier('../info/feature_animeface/lbpcascade_animeface.xml')
        # 顔画像リスト
        self.face_img_list = []
        
    def pixiv_download_illustrators(self, save_path):
        """
        記録してあるイラストレータの画像すべてをダウンロード
        """
        using_illust_path = '../info/follow_user_account/user_account_using.json' # ユーザ情報保存先
        # user情報取得
        user_id_list = self.__get_user_id_list(using_illust_path)

        for user_id in user_id_list:
            self.pixiv_download_illusts(save_path, user_id)

    def pixiv_download_illusts(self, save_path, user_id):
        """
        引数のIDのイラストレータの画像をすべてダウンロード
        """
        # ユーザを指定し、JSON取得
        works_info = self.p_api.users_works(user_id, per_page=300)

        # ユーザのディレクトリがなければ作成
        user_path = save_path + str(user_id) + '/'
        self.__make_directory(user_path)

        # ダウンロード
        print('start download\n')
        for work_info in works_info.response:
            # DL済みの画像かどうか判定
            if not os.path.exists(user_path + work_info.image_urls.large.split('/')[-1]):
                # タイトル出力
                print(work_info.title.replace("/", "-")) # '/'はPathとして扱われるため回避
                # 保存
                self.p_aapi.download(work_info.image_urls.large, path=user_path)
                # マナー
                time.sleep(1)
        print('\nfinish download\n')

    # 複数のイラストレータごとにトリミング
    def triming_face_illlustrators(self, save_path):
        """
        記録してあるイラストレータの画像すべてをトリミング
        """
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
            self.triming_face_illusts(save_path, illust_path_list, user_id)

    # 一人のイラストレータのイラストをトリミング
    def triming_face_illusts(self, save_path, illust_list, user_id):
        """
        引数のIDのイラストレータの画像をすべてトリミング
        """
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
                self.__save_face_illust(path, face_img)

    def get_face_illust(self):
        return self.face_img_list

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
    
    def __save_face_illust(self, path, face_img):
        if not os.path.exists(path): # DL済みの画像かどうか判定
            # リサイズ
            resize_face_img = self.__resize_face_illust(face_img, 64)
            # 保存
            cv2.imwrite(path, resize_face_img) 
            print(path + 'をトリミングし保存しました')
            self.face_img_list.append(face_img)

    def __resize_face_illust(self, face_img, size):
        width, height = size, size
        resize_face_img = cv2.resize(face_img, (width, height))
        return resize_face_img

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
    from pixivpy3 import *
    from Infomation import Information

    my_account_path = '../info/my_account/my_account.json' # 自分のアカウント情報保存先
    info = Information(my_account_path)
    p_id, pw, u_id = info.get_my_pixiv_account()
    
    pixiv_api = PixivAPI()
    pixiv_aapi = AppPixivAPI()
    pixiv_api.login(p_id, pw)
    pixiv_aapi.login(p_id, pw)

    ils = Illust(pixiv_api, pixiv_aapi)
    
    # test1
    # ils.pixiv_download_illustrators('../data/pixiv/row/dl_test/')

    # # test2
    # shirabi = 216403
    # ils.pixiv_download_illusts('../data/pixiv/row/dl_test/', shirabi)

    # # test3
    # ils.triming_face_illlustrators('../data/pixiv/interim/face/face_test/')
    
    # # test4
    kantoku = 1565632
    ils.triming_face_illusts('../data/pixiv/interim/face/face_test/', ['../data/pixiv/interim/face/face_test/test_kantoku.jpg'], kantoku)
    
    # # test5
    print(ils.get_face_illust())