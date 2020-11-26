class PixivInfo:

    def __init__(self, json_obj):
        self.P_ID = self.json_obj['pixiv_id']
        self.PW   = self.json_obj['password']
        self.U_ID = self.json_obj['user_id']

