import os
import json
import time
import pandas as pd
from UserRecord import UserRecord
from Login import Login
from pixivpy3 import *

class DownloadIllust:

    def __init__(self, user_record, api):

        # pixiv api
        self.p_api, self.p_aapi = api.get_pixvi_api()
        # UserRecord
        self.ur = user_record

    def download(self, path):
        # user情報取得
        df = self.ur.get_user_record(path)
        user_id_list = df['user_id'].values
        
        # イラスト保存先
        save_path = '../data/pixiv/row/'

        for user_id in user_id_list:
            # ユーザを指定し、JSON取得
            json_result = self.p_api.users_works(user_id, per_page=300)

            # ユーザのディレクトリがなければ作成
            user_path = save_path+str(user_id)
            if not os.path.exists(user_path):
                os.mkdir(user_path)

            # ダウンロード
            for img in json_result.response:
                self.p_aapi.download(img.image_urls.large, path=user_path)
                time.sleep(1)