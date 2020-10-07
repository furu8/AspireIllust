import os.path
import json
import pandas as pd

class UserRecord:

    def __init__(self):
        # ユーザ情報
        self.user_df = pd.DataFrame(columns=['user_id', 'user_name'])
        self.user_id_list = []
        self.user_name_list = []

    # ユーザ情報保存
    def save_user_record(self, path):
        self.user_df['user_id'] = self.user_id_list
        self.user_df['user_name'] = self.user_name_list
        self.user_df.to_json(path)
        print(path+'に保存しました')

    # ユーザ情報取得
    def get_user_record(self, path):
        df = pd.read_json(path)
        return df

    # 自分のフォロー欄の情報を記録
    def register_user_record(self, u_id, p_aapi):
        json_result = p_aapi.user_following(u_id) 
        
        # JSONデータをリストに記録 
        for result in json_result.user_previews:
            self.user_id_list.append(result.user.id)
            self.user_name_list.append(result.user.name)

# テスト
if __name__ == "__main__":
    from pixivpy3 import *
    from Infomation import Information

    myaccount_path = '../info/my_account/pixiv_my_account.json' # 自分のアカウント情報保存先
    info = Information(myaccount_path)
    p_id, pw, u_id = info.get_my_pixiv_account()
    
    p_aapi = AppPixivAPI()
    p_aapi.login(p_id, pw)

    ur = UserRecord()
    # test1
    ur.register_user_record(u_id, p_aapi)
    # test2
    path = '../info/follow_user_account/pixiv_test_user_account.json'
    ur.save_user_record(path)
    # test3
    df = ur.get_user_record(path)
    print(df)