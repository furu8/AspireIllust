from pixivpy3 import *
import json
import pandas as pd
from Login import Login
from UserRecord import UserRecord
from DownloadIllust import DownloadIllust

if __name__ == "__main__":
    api = Login()
    ur = UserRecord()
    dl = DownloadIllust()

    # pixivログイン
    self.api = Login()
    self.api.pixiv_login(self.p_id, self.pw)

    # ユーザ情報を保存
    # ur.post_user_record('../info/follow_user_account/user_account.json') # 新しくフォローしたら作動

    # ユーザのイラストを保存
    dl.download('../info/follow_user_account/user_account_using.json')