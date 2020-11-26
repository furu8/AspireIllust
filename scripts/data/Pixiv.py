from pixivpy3 import *

class Pixiv:

    def __init__(self, pixiv_json):
        # ユーザ情報
        self.P_ID = pixiv_json['pixiv_id']
        self.PW   = pixiv_json['password']
        self.U_ID = pixiv_json['user_id']

        # pixiv_api
        self.pixiv_api = PixivAPI()
        self.pixiv_aapi = AppPixivAPI()

        # ログイン
        self.pixiv_api.login(self.P_ID, self.PW)
        self.pixiv_aapi.login(self.P_ID, self.PW)

        #UserRecordの保存先
        self.user_record_path = '../../info/my_account/pixiv_my_account.json'

    # ユーザ情報取得
    def get_user_record(self):
        df = pd.read_json(self.user_record_path)
        return df

    # 自分のフォロー欄の情報を記録
    def register_user_record(self):
        # フォローユーザ取得
        follow_json = self.pixiv_aapi.user_following(self.U_ID) 
        
        # JSONデータをリストに記録 
        user_id_list, user_name_list = self.__add_id_name(follow_json):

        # 保存
        self.__save_user(self, user_id_list, user_name_list):

    def __add_id_name(self, follow_json):
        user_id_list = []
        user_name_list = []

        for result in follow_json.user_previews:
            user_id_list.append(result.user.id)
            user_name_list.append(result.user.name)

        return user_id_list, user_name_list

    def __save_user(self, user_id_list, user_name_list):
        self.user_df['user_id'] = user_id_list
        self.user_df['user_name'] = user_name_list
        self.user_df.to_json(path)

        print(self.user_record_path + 'に保存しました')


