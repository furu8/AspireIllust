from pixivpy3 import *

class Login:

    def __init__(self):
        # pixiv_api
        self.pixiv_api = PixivAPI()
        self.pixiv_aapi = AppPixivAPI()

    def pixiv_login(self, p_id, pw):
        # ログイン
        self.pixiv_api.login(p_id, pw)
        self.pixiv_aapi.login(p_id, pw)
    
