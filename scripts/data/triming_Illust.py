import os
import cv2
import pandas as pd
import glob as gb

# 複数のイラストレータごとにトリミング
def triming_illlustrator_face_illusts():
    """
    記録してあるイラストレータの画像すべてをトリミング
    """
    # ユーザ情報取得
    using_illust_path = '../../info/follow_user_account/pixiv_user_account_using.json' 
    user_df = df = pd.read_json(using_illust_path)
    
    # イラストレータごと
    for user_id in user_df['user_id'].values:
        # イラストレータごとのパスを指定
        illustrator_path = '../../data/pixiv/raw/' + str(user_id) + '/*'
        # イラストのリスト
        illust_list = gb.glob(illustrator_path)
        # イラストごとにトリミング
        triming_face_illusts(illust_list, user_id)

# 一人のイラストレータのイラストをトリミング
def triming_face_illusts(illust_list, user_id):
    """
    引数のIDのイラストレータの画像をすべてトリミング
    """
    # イラストごと
    for illust in illust_list:
        # 保存するファイル名
        save_file_name = illust.split('/')[-1].split('.')[0]
        print(save_file_name)
        # 顔抽出
        img, face_list = get_face_img(illust)
        
        if len(face_list) == 0:
            continue
        # キャラごと
        for i, face in enumerate(face_list):
            x, y, w, h = face # x始点、y始点、w幅、h高さ
            face_img = img[y:y+h, x:x+w] # トリミング
            # ユーザのディレクトリがなければ作成
            save_path = '../../data/pixiv/interim/face/' + str(user_id) + '/'
            make_directory(save_path)
            # pngで保存
            user_save_path = save_path + save_file_name + '_' + str(i+1) + '.png'
            save_face_illust(user_save_path, face_img)

# ディレクトリがなければ作成
def make_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print('{}にディレクトリ作成'.format(path))

def save_face_illust(path, face_img):
    if not os.path.exists(path): # DL済みの画像かどうか判定
        # リサイズ
        resize_face_img = resize_face_illust(face_img, 64)
        # 保存
        cv2.imwrite(path, resize_face_img) 
        print(path + 'をトリミングし保存しました')

def resize_face_illust(face_img, size):
    width, height = size, size
    resize_face_img = cv2.resize(face_img, (width, height))
    
    return resize_face_img

# 顔抽出
def get_face_img(illust):
    # animeface
    cascade = cv2.CascadeClassifier('../../info/feature_animeface/lbpcascade_animeface.xml')
    
    img = cv2.imread(illust, cv2.IMREAD_COLOR) # デフォルトカラー読み込み
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # グレースケール化
    gray_img = cv2.equalizeHist(gray_img) # ヒストグラム平均化（見やすくなる）
    
    face_list = cascade.detectMultiScale(gray_img, scaleFactor=1.01, minNeighbors=5, minSize=(24, 24)) # 見逃しを極力少なくパラメータ設定した場合
    # face_list = cascade.detectMultiScale(gray_img, scaleFactor=1.09, minNeighbors=5, minSize=(24, 24)) # 誤検知を極力少なくパラメータ設定した場合
    
    return img, face_list

if __name__ == "__main__":
    # import matplotlib.pyplot as plt
    # illust = '../../data/pixiv/raw/216403/83914155_p0.jpg'
    # img, face_list = get_face_img(illust)
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # plt.show()

    # トリミング実行
    triming_illlustrator_face_illusts()
