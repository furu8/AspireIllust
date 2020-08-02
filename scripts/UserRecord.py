import os.path
import json
import pandas as pd

class UserRecord:

    def __init__(self, p_api, p_aapi):
        # pixiv api
        self.p_api = p_api
        self.p_aapi = p_aapi
        # ユーザ情報
        self.user_df = pd.DataFrame(columns=['user_id', 'user_name'])

    def post_user_record(self, path, u_id):
        user_id_list = []
        user_name_list = []

        # 自分のフォロー欄の情報を取得
        json_result = self.p_aapi.user_following(u_id) 

        # JSONに記録 
        for result in json_result.user_previews:
            user_id_list.append(result.user.id)
            user_name_list.append(result.user.name)
        # 保存
        self.user_df['user_id'] = user_id_list
        self.user_df['user_name'] = user_name_list
        self.user_df.to_json(path)

    def get_user_record(self, path):
        df = pd.read_json(path)
        return df