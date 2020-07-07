from pixivpy3 import *
import os
import json
import pandas as pd
from UserRecord import UserRecord

class DownloadIllust:

    def __init__(self):
        # pixivのアカウント情報を取得
        my_account_path = '../info/my_account/my_account.json'
        json_file = open(my_account_path, 'r')
        json_obj = json.load(json_file)
        self.p_id = json_obj['pixiv_id']
        self.pw = json_obj['password']
        self.u_id = json_obj['user_id']

        # ログイン
        self.aapi = AppPixivAPI()
        self.aapi.login(self.p_id, self.pw)
        
        # UserRecord
        self.ur = UserRecord()

    def download(self):
        # user情報取得
        df = self.ur.get_user_record()
        user_id_list = df['user_id'].values
        
        # イラスト保存先
        path = '../data/pixiv/row/'

        for user_id in user_id_list:
            # ユーザを指定
            img = self.aapi.user_illusts(user_id)
            # ユーザのディレクトリがなければ作成
            user_path = path+str(user_id)
            if not os.path.exists(user_path):
                os.mkdir(user_path)
            # ダウンロード
            for img in img.illusts:
                self.aapi.download(img.image_urls.large, path=user_path)

if __name__ == "__main__":
    dli = DownloadIllust()
    dli.download()