import tweepy
import pandas as pd

class Twitter:

    def __init__(self, twitter_json):
        # ユーザ情報 twitter token
        self.CONSUMER_KEY        = twitter_json['API_key']
        self.CONSUMER_SECRET_KEY = twitter_json['API_secret_key']
        self.ACCESS_TOKEN        = twitter_json['Access_token']
        self.ACCESS_TOKEN_SECRET = twitter_json['Access_token_secret']

        # twitter api
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET_KEY)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.my_info = self.api.me()
        
        # ユーザのアカウント情報データフレーム
        self.user_df = pd.DataFrame(columns=['user_id', 'user_name'])


    # def download_illustrator_illusts(self, load_path=None):
    #     """
    #     記録してあるイラストレータの画像すべてをダウンロード
    #     """
    #     # ユーザ情報取得
    #     if not load_path is None:
    #         # using_illust_path = '../../info/follow_user_account/pixiv_user_account_using.json' 
    #         self.user_df = self.__get_user_record_path(load_path)
    #     elif self.user_df.empty:
    #         print('user_dfが空なため、register_user_recordメソッドを実行します')
    #         self.register_user_record()

    #     # ダウンロード実行
    #     for user_id in self.user_df['user_id'].values:
    #         self.download_illusts(user_id)            


    # def download_illusts(self, user_id):
    #     """
    #     引数のIDのイラストレータの画像をすべてダウンロード
    #     """
    #     # ユーザを指定し、JSON取得
    #     works_info = self.pixiv_api.users_works(user_id, per_page=300)

    #     # ユーザのディレクトリがなければ作成
    #     save_path = '../../data/pixiv/row/' + str(user_id) + '/'
    #     self.__make_directory(save_path)

    #     # ダウンロード
    #     print('start download\n')
    #     for work_info in works_info.response:
    #         # DL済みの画像かどうか判定
    #         if not os.path.exists(save_path + work_info.image_urls.large.split('/')[-1]):
    #             # タイトル出力
    #             print(work_info.title.replace("/", "-")) # '/'はPathとして扱われるため回避
    #             # 保存
    #             self.pixiv_aapi.download(work_info.image_urls.large, path=save_path)
    #             # マナー
    #             time.sleep(1)
    #     print('\nfinish download\n')
    

    # # ディレクトリがなければ作成
    # def __make_directory(self, path):
    #     if not os.path.exists(path):
    #         os.mkdir(path)
    #         print('{}にディレクトリ作成'.format(path))


    # # pathからユーザ情報取得
    # def __get_user_record_path(self, path):
    #     """
    #     引数pathにはuser_account.jsonとuser_account_using.jsonを指定
    #     """
    #     return pd.read_json(path)


    # 自分のフォロー欄の情報を記録
    def register_user_record(self, save_path=None):
        # フォローユーザ取得
        follow_user_ids = tweepy.Cursor(self.api.friends_ids, user_id=self.my_info.id).items()
        
        # JSONデータをリストに記録 
        user_id_list, user_name_list, user_screen_name_list = self.__add_id_name(follow_user_ids)

        # 登録
        self.user_df['user_id'] = user_id_list
        self.user_df['user_name'] = user_name_list
        # self.user_df['user_sceen_name'] = user_screen_name_list

        # 保存
        if not save_path is None:
            self.user_df.to_json(save_path)
            print(save_path + 'に保存しました')
            

    def __add_id_name(self, follow_user_ids):
        user_id_list = []
        user_name_list = []
        user_screen_name_list = []

        for user_id in follow_user_ids:
            user_id_list.append(user_id)
            user_name_list.append(self.api.get_user(user_id).name)
            user_screen_name_list.append(self.api.get_user(user_id).screen_name)

        return user_id_list, user_name_list, user_screen_name_list

if __name__ == "__main__":
    from Infomation import Information
    info = Information()
    twitter_json = info.get_twitter_json()

    twitter = Twitter(twitter_json)
    # twitter.register_user_record('../../info/follow_user_account/twitter_user_account.json')
    twitter.register_user_record()
    print(twitter.user_df)
    
