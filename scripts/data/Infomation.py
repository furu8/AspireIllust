import json
import sys

class Information:

    def __init__(self, path):
        # 引数のファイルをJSONオブジェクトとしてもつ
        self.my_account_path = path
        self.json_obj = self.__read_json()
    
    def get_pixiv_info(self):
        try:
            P_ID = self.json_obj['pixiv_id']
            PW   = self.json_obj['password']
            U_ID = self.json_obj['user_id']
        except KeyError:
            print('Pixivのjson_objではありません')
            sys.exit(1)
        
        return P_ID, PW, U_ID

    def get_twitter_info(self):
        try:
            CONSUMER_KEY        = self.json_obj['API_key']
            CONSUMER_SECRET_KEY = self.json_obj['API_secret_key']
            ACCESS_TOKEN        = self.json_obj['Access_token']
            ACCESS_TOKEN_SECRET = self.json_obj['Access_token_secret']
        except KeyError:
            print('Twitterのjson_objではありません')
            sys.exit(1)

        return CONSUMER_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

    def __read_json(self):
        with open(self.my_account_path) as json_file:
            json_obj = json.load(json_file)

        return json_obj

# テスト
if __name__ == "__main__":
    my_account_path = '../../info/my_account/pixiv_my_account.json' # 自分のアカウント情報保存先
    pixiv_info = Information(my_account_path)
    P_ID, PW, U_ID = pixiv_info.get_pixiv_info()
    print(P_ID, PW, U_ID)

    my_account_path = '../../info/my_account/twitter_my_account.json' # 自分のアカウント情報保存先
    twitter_info = Information(my_account_path)
    CONSUMER_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = twitter_info.get_twitter_info()
    print(CONSUMER_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)