import tweepy

class Twitter:

    def __init__(self, twitter_json):
        # ユーザ情報 twitter token
        self.CONSUMER_KEY        = twitter_json['API_key']
        self.CONSUMER_SECRET_KEY = twitter_json['API_secret_key']
        self.ACCESS_TOKEN        = twitter_json['Access_token']
        self.ACCESS_TOKEN_SECRET = twitter_json['Access_token_secret']

        # twitter api
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        self.twitter_api = tweepy.API(auth, wait_on_rate_limit = True)

        # UserRecordの保存先
        
        # ユーザのアカウント情報データフレーム