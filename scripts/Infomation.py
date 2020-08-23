import json

class Information:

    def __init__(path):
        # pixivのアカウント情報を取得
        my_account_path = path
        with open(my_account_path) as json_file:
            self.json_obj = json.load(json_file)
    
    def get_my_pixiv_account(self):
        p_id = self.json_obj['pixiv_id']
        pw = self.json_obj['password']
        u_id = self.json_obj['user_id']
    
        return p_id, pw, u_id