from pixivpy3 import *

class API:

    def __init__(self):
        # pixiv_api
        self.pixiv_api = PixivAPI()
        self.pixiv_aapi = AppPixivAPI()

    def pixiv_login(self, p_id, pw):
        # ログイン
        self.pixiv_api.login(p_id, pw)
        self.pixiv_aapi.login(p_id, pw)
    
    def get_pixvi_api(self):
        return self.pixiv_api, self.pixiv_aapi
    
