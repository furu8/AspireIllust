import json
import pandas as pd
from Infomation import Information
from Login import Login
from UserRecord import UserRecord
from DownloadIllust import DownloadIllust
from Face import Face

if __name__ == "__main__":
    # pixivのアカウント情報を取得
    info = Information()
    p_id, pw, u_id = info.get_my_pixiv_account()

    # pixivログイン
    api = Login()
    api.pixiv_login(p_id, pw)
    # pixiv api
    p_api, p_aapi = api.get_pixvi_api()

    # ユーザ情報を保存
    ur = UserRecord(p_api, p_aapi)
    # ur.post_user_record('../info/follow_user_account/user_account.json', u_id) # 新しくフォローしたら作動

    # ユーザのイラストを保存
    using_illust_json_path = '../info/follow_user_account/user_account_using.json'
    dl = DownloadIllust(ur, api)
    dl.pixiv_download(using_illust_json_path)

    # イラストの顔を抽出
    # face = Face('../info/follow_user_account/user_account_using.json')
    # face.triming_face('../data/pixiv/interim/face/')