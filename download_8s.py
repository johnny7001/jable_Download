import os
import pymysql
import requests
import json

content = {}


# 獲取8s影片網址
def get_mysql(dirName):
    # def mysql(url):
    # 開啟資料庫連線
    url = f'http://127.0.0.1:3123/videos/{dirName}'
    r = requests.post(url)
    data = json.loads(r.text)
    short_url = data['short_url']
    print(short_url)
    return short_url

# 執行8s_mp4下載


def download_file(name, short_url):
    folder = name
    filename = name + "_8s.mp4"
    print(short_url)
    print(f'jableTV/{folder}/{filename}')
    r = requests.get(short_url)
    print("****Connected****")
    f = open(f'jableTV/{folder}/{filename}', 'wb')
    print("下載中...")
    for chunk in r.iter_content(chunk_size=255):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
    print(f"{name}的短片下載完成")
    f.close()

# 檢查檔案是否存在並下載


def main_8s(dirName, short_url):
    try:
        # 若資料夾存在
        if os.path.exists('jableTV/' + dirName):
            # 假設8秒影片不存在
            if not os.path.isfile(f'jableTV/{dirName}/{dirName}_8s.mp4'):
                download_file(dirName, short_url)  # 8秒短片下載
                print(f'下載{dirName}的8秒短片')
            else:
                print(dirName, '的8秒短片已下載')
        else:
            # 創建資料夾
            os.mkdir('jableTV/' + dirName)
            download_file(dirName, short_url)  # 8秒短片下載
            print(f'下載{dirName}的8秒短片')
    except:
        print('下載失敗')


if __name__ == "__main__":
    print('開始下載')
    # https://jable.tv/videos/abp-835/s
    dirName = 'abp-835'
    # url = 'https://jable.tv/videos/ipx-907/'
    # urlSplit = url.split('/')
    # dirName = urlSplit[-2]
    # print(dirName)
    short_url = get_mysql(dirName)
    print(short_url)
    # download_file(dirName, short_url)
    main_8s(dirName, short_url)
