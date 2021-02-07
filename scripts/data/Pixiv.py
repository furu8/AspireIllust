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

        # ユーザのアカウント情報データフレーム
        self.user_df = pd.DataFrame(columns=['user_id', 'user_name'])


    def download_illustrator_illusts(self, load_path=None):
        """
        記録してあるイラストレータの画像すべてをダウンロード
        """
        # ユーザ情報取得
        if not load_path is None:
            # using_illust_path = '../../info/follow_user_account/pixiv_user_account_using.json' 
            self.user_df = self.__get_user_record_path(load_path)
        elif self.user_df.empty:
            print('user_dfが空なため、register_user_recordメソッドを実行します')
            self.register_user_record()

        # ダウンロード実行
        for user_id in self.user_df['user_id'].values:
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


    # pathからユーザ情報取得
    def __get_user_record_path(self, path):
        """
        引数pathにはuser_account.jsonとuser_account_using.jsonを指定
        """
        return pd.read_json(path)


    # 自分のフォロー欄の情報を記録
    def register_user_record(self, save_path=None):
        # フォローユーザ取得
        follow_json = self.pixiv_aapi.user_following(self.U_ID) 
        
        # JSONデータをリストに記録 
        user_id_list, user_name_list = self.__add_id_name(follow_json)

        # 登録
        self.user_df['user_id'] = user_id_list
        self.user_df['user_name'] = user_name_list

        # 保存
        # # UserRecordの保存先
        # self.user_record_path = '../../info/follow_user_account/pixiv_user_account.json'
        if not save_path is None:
            self.user_df.to_json(save_path)
            print(save_path + 'に保存しました')
            

    def __add_id_name(self, follow_json):
        user_id_list = []
        user_name_list = []

        for result in follow_json.user_previews:
            user_id_list.append(result.user.id)
            user_name_list.append(result.user.name)

        return user_id_list, user_name_list

        
if __name__ == "__main__":
    from Infomation import Information
    info = Information()
    pixiv_json = info.get_pixiv_json()
    pixiv = Pixiv(pixiv_json)
    pixiv.register_user_record()
    print(pixiv.user_df)
    pixiv.download_illustrator_illusts()