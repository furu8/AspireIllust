import os
import json
import time
import pandas as pd
from UserRecord import UserRecord

class DownloadIllust:

    def __init__(self, p_api, p_aapi):
        # pixiv api
        self.p_api = p_api
        self.p_aapi = p_aapi
        # UserRecord
        self.ur = UserRecord()
        

    def pixiv_download(self, path):
        # user情報取得
        df = self.ur.get_user_record(path)
        user_id_list = df['user_id'].values
        
        # イラスト保存先
        save_path = '../data/pixiv/row/'

        for user_id in user_id_list:
            # ユーザを指定し、JSON取得
            works_info = self.p_api.users_works(user_id, per_page=300)

            # ユーザのディレクトリがなければ作成
            user_path = save_path+str(user_id)
            if not os.path.exists(user_path):
                os.mkdir(user_path)

            # ダウンロード
            print('start download\n')
            for work_info in works_info.response:
                # タイトル出力
                print(work_info.title.replace("/", "-")) # '/'はPathとして扱われるため回避
                # 保存
                self.p_aapi.download(work_info.image_urls.large, path=user_path)
                # マナー
                time.sleep(1)
            print('finish download')