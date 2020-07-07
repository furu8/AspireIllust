from pixivpy3 import *
import os.path
import json
import pandas as pd

class UserRecord:

    def __init__(self):
        # pixivのアカウント情報を取得
        path = '../info/my_account/my_account.json'
        json_file = open(path, 'r')
        json_obj = json.load(json_file)
        self.p_id = json_obj['pixiv_id']
        self.pw = json_obj['password']
        self.u_id = json_obj['user_id']
        # ログイン
        self.aapi = AppPixivAPI()
        self.aapi.login(self.p_id, self.pw)
        # ユーザ情報
        self.user_df = pd.DataFrame(columns=['user_id', 'user_name'])

    def post_user_record(self):
        user_id_list = []
        user_name_list = []

        json_result = self.aapi.user_following(self.u_id) # 自分のフォロー欄の情報を取得

        for result in json_result.user_previews:
            user_id_list.append(result.user.id)
            user_name_list.append(result.user.name)
        
        self.user_df['user_id'] = user_id_list
        self.user_df['user_name'] = user_name_list

        self.user_df.to_json('../info/follow_user_account/user_account.json')

if __name__ == "__main__":
    ur = UserRecord()
    ur.post_user_record()