import json
import pandas as pd
from Infomation import Information
from API import API
from UserRecord import UserRecord
from Illust import Illust

def pixiv_my_account_info():
    my_account_path = '../info/my_account/my_account.json' # 自分のアカウント情報保存先
    info = Information(my_account_path)
    p_id, pw, u_id = info.get_my_pixiv_account()

    return p_id, pw, u_id    

def pixiv_user_account_info(u_id, p_aapi):
    user_account_path = '../info/follow_user_account/user_account.json' # ユーザのアカウント情報保存先
    ur = UserRecord()
    ur.register_user_record(u_id, p_aapi) # 登録
    ur.save_user_record(user_account_path) # 保存

def pixiv_api(p_id, pw):
    api = API()
    api.pixiv_login(p_id, pw) # ログイン
    p_api, p_aapi = api.get_pixvi_api() # api
    
    return p_api, p_aapi

def pixiv_download(ils):
    save_path = '../data/pixiv/row/' # 保存先
    ils.pixiv_download_illustrators(save_path)

def triming_illusts(ils):
    save_path = '../data/pixiv/interim/face/' # 保存先
    ils.triming_face_illlustrators(save_path)

def main():
    # pixivのアカウント情報を取得
    p_id, pw, u_id = pixiv_my_account_info()

    # pixiv api
    p_api, p_aapi = pixiv_api(p_id, pw)

    # ユーザ情報を登録・保存
    pixiv_user_account_info(u_id, p_aapi)
    
    # pixivイラストを保存
    ils = Illust(p_api, p_aapi) 
    pixiv_download(ils)

    # イラストの顔を抽出
    triming_illusts(ils) 
    

if __name__ == "__main__":
    main()