import json

class Information:

    def __init__(self):
        # pixivのアカウント情報を取得
        my_account_path = '../info/my_account/my_account.json'
        with open(my_account_path) as json_file:
            self.json_obj = json.load(json_file)
    
    def get_my_pixiv_account(self):
        p_id = json_obj['pixiv_id']
        pw = json_obj['password']
        u_id = json_obj['user_id']
    
        return p_id, pw, u_id