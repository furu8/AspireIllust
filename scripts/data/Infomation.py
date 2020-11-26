import json
import sys

class Information:

    def __init__(self):
        # 引数のファイルをJSONオブジェクトとしてもつ
        self.pixiv_my_account_path = '../../info/my_account/pixiv_my_account.json'
        self.twitter_my_account_path = '../../info/my_account/twitter_my_account.json'

        self.pixiv_json_obj = self.__read_json(self.pixiv_my_account_path)
        self.twitter_json_obj = self.__read_json(self.twitter_my_account_path)
    
    def get_pixiv_obj(self):
        return self.pixiv_json_obj

    def get_twitter_obj(self):
        return self.twitter_json_obj

    def __read_json(self, my_account_path):
        with open(my_account_path) as json_file:
            json_obj = json.load(json_file)

        return json_obj

# テスト
if __name__ == "__main__":
    info = Information()
    print(info.get_pixiv_obj())
    print(info.get_twitter_obj())