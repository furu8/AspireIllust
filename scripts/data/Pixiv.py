from pixivpy3 import *
import pandas as pd
import os, time

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

        # UserRecordの保存先
        self.user_record_path = '../../info/follow_user_account/pixiv_user_account.json'

        # ユーザのアカウント情報データフレーム
        self.user_df = pd.DataFrame(columns=['user_id', 'user_name'])

    # ユーザ情報取得
    def get_user_record(self, path):
        """
        引数pathにはuser_account.jsonとuser_account_using.jsonを指定
        """
        df = pd.read_json(path)
        return df

    # 自分のフォロー欄の情報を記録
    def register_user_record(self):
        # フォローユーザ取得
        follow_json = self.pixiv_aapi.user_following(self.U_ID) 
        
        # JSONデータをリストに記録 
        user_id_list, user_name_list = self.__add_id_name(follow_json)

        # 保存
        self.__save_user(user_id_list, user_name_list)

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
        self.user_df.to_json(self.user_record_path)

        print(self.user_record_path + 'に保存しました')

    def download_illustrator_illusts(self):
        """
        記録してあるイラストレータの画像すべてをダウンロード
        """
        # ユーザ情報取得
        using_illust_path = '../../info/follow_user_account/pixiv_user_account_using.json' 
        user_df = self.get_user_record(using_illust_path)
        
        for user_id in user_df['user_id'].values:
            self.download_illusts(user_id)

    def download_illusts(self, user_id):
        """
        引数のIDのイラストレータの画像をすべてダウンロード
        """
        # ユーザを指定し、JSON取得
        works_info = self.pixiv_api.users_works(user_id, per_page=300)

        # ユーザのディレクトリがなければ作成
        save_path = '../../data/pixiv/row/' + str(user_id) + '/'
        self.__make_directory(save_path)

        # ダウンロード
        print('start download\n')
        for work_info in works_info.response:
            # DL済みの画像かどうか判定
            if not os.path.exists(save_path + work_info.image_urls.large.split('/')[-1]):
                # タイトル出力
                print(work_info.title.replace("/", "-")) # '/'はPathとして扱われるため回避
                # 保存
                self.pixiv_aapi.download(work_info.image_urls.large, path=save_path)
                # マナー
                time.sleep(1)
        print('\nfinish download\n')
    
    # ディレクトリがなければ作成
    def __make_directory(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
            print('{}にディレクトリ作成'.format(path))


if __name__ == "__main__":
    from Infomation import Information
    info = Information()
    pixiv_json = info.get_pixiv_json()
    pixiv = Pixiv(pixiv_json)
    # pixiv.register_user_record()
    # print(pixiv.get_user_record())
    pixiv.download_illustrator_illusts()


