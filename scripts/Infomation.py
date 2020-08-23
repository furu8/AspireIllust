import json

class Information:

    def __init__(self, path):
        # pixivのアカウント情報を取得
        my_account_path = path
        with open(my_account_path) as json_file:
            self.json_obj = json.load(json_file)
    
    def get_my_pixiv_account(self):
        p_id = self.json_obj['pixiv_id']
        pw = self.json_obj['password']
        u_id = self.json_obj['user_id']
    
        return p_id, pw, u_id

# テスト
if __name__ == "__main__":
    myaccount_path = '../info/my_account/my_account.json' # 自分のアカウント情報保存先
    info = Information(myaccount_path)
    p_id, pw, u_id = info.get_my_pixiv_account()
    
    print(p_id, pw, u_id)