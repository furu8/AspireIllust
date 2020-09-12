import os
import json
import time
import pandas as pd
from UserRecord import UserRecord

class Illust:

    def __init__(self, p_api, p_aapi):
        # pixiv api
        self.p_api = p_api
        self.p_aapi = p_aapi
        # UserRecord
        self.ur = UserRecord()
        
    def pixiv_download(self, save_path):
        using_illust_path = '../info/follow_user_account/user_account_using.json' # ユーザ情報保存先
        # user情報取得
        user_id_list = self.__get_user_id_list(using_illust_path)

        for user_id in user_id_list:
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

    dl = Illust(pixiv_api, pixiv_aapi)
    # test1
    dl.pixiv_download('../data/pixiv/row/dl_test/')