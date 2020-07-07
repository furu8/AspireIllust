from pixivpy3 import *
import os.path
import json
import pandas as pd

class UserRecord:

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

        # ユーザ情報
        self.user_df = pd.DataFrame(columns=['user_id', 'user_name'])

    def post_user_record(self, path):
        user_id_list = []
        user_name_list = []

        # 自分のフォロー欄の情報を取得
        json_result = self.aapi.user_following(self.u_id) 

        # JSONに記録 
        for result in json_result.user_previews:
            user_id_list.append(result.user.id)
            user_name_list.append(result.user.name)
        
        self.user_df['user_id'] = user_id_list
        self.user_df['user_name'] = user_name_list
        self.user_df.to_json(path)

    def get_user_record(self, path):
        df = pd.read_json(path)
        return df