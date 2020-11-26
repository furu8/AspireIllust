import json
import pandas as pd
from Infomation import Information
from API import API
from UserRecord import UserRecord
from Illust import Illust

def get_my_pixiv_account_info():
    pixiv_my_account_path = '../../info/my_account/pixiv_my_account.json' # 自分のアカウント情報保存先
    pixiv_info = Information(pixiv_my_account_path)
    P_ID, PW, U_ID = pixiv_info.get_pixiv_info()

    return P_ID, PW, U_ID

def get_my_twitter_account_info():
    twitter_my_account_path = '../../info/my_account/twitter_my_account.json' # 自分のアカウント情報保存先
    twitter_info = Information(twitter_my_account_path)
    CONSUMER_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = twitter_info.get_twitter_info()

    return CONSUMER_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

def pixiv_user_account_info(u_id, p_aapi):
    user_account_path = '../info/follow_user_account/pixiv_user_account.json' # ユーザのアカウント情報保存先
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
    P_ID, PW, U_ID = get_my_pixiv_account_info()

    # twitterのアカウント情報を取得
    CONSUMER_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = get_my_twitter_account_info()
    
    # pixiv api
    p_api, p_aapi = pixiv_api(P_ID, PW)

    # ユーザ情報を登録・保存
    pixiv_user_account_info(u_id, p_aapi)
    
    # pixivイラストを保存
    ils = Illust(p_api, p_aapi) 
    pixiv_download(ils)

    # イラストの顔を抽出
    triming_illusts(ils) 
    

if __name__ == "__main__":
    main()