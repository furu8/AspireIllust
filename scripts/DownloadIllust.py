from pixivpy3 import *
import os.path
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
        df = self.ur.get_user_record()

        print(df)
    
    # def extract_user(self):

if __name__ == "__main__":
    dli = DownloadIllust()
    dli.download()