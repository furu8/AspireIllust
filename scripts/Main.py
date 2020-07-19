from pixivpy3 import *
import json
import pandas as pd
from UserRecord import UserRecord
from DownloadIllust import DownloadIllust

if __name__ == "__main__":
    ur = UserRecord()
    dl = DownloadIllust()

    # ユーザ情報を保存
    ur.post_user_record('../info/follow_user_account/user_account.json')

    # ユーザのイラストを保存
    dl.download('../info/follow_user_account/user_account_using.json')