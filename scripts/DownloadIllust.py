import os
import json
import time
import pandas as pd
from UserRecord import UserRecord
from Login import Login

class DownloadIllust:

    def __init__(self):
        # pixivのアカウント情報を取得
        my_account_path = '../info/my_account/my_account.json'
        json_file = open(my_account_path, 'r')
        json_obj = json.load(json_file)
        self.p_id = json_obj['pixiv_id']
        self.pw = json_obj['password']
        self.u_id = json_obj['user_id']

        # pixivログイン
        self.api = Login()
        self.api.pixiv_login(self.p_id, self.pw)
        
        # UserRecord
        self.ur = UserRecord()

    def download(self, path):
        # user情報取得
        df = self.ur.get_user_record(path)
        user_id_list = df['user_id'].values
        
        # イラスト保存先
        save_path = '../data/pixiv/row/'

        for user_id in user_id_list:
            # ユーザを指定し、JSON取得
            json_result = self.api.pixiv_api.users_works(user_id, per_page=300)

            # ユーザのディレクトリがなければ作成
            user_path = save_path+str(user_id)
            if not os.path.exists(user_path):
                os.mkdir(user_path)

            # ダウンロード
            for img in json_result.response:
                self.api.pixiv_aapi.download(img.image_urls.large, path=user_path)
                time.sleep(1)