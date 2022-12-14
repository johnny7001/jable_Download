import json
import os
import pymysql
import requests


def get_mysql_data(dirName):
    # 開啟資料庫連線
    url = f'http://127.0.0.1:3123/videos/{dirName}'
    r = requests.post(url)
    results = json.loads(r.text)
    return results


def storge_json(results):
    video_data = {}

    dirName = results['dir_name']
    try:
        video_data["header"] = results['header']
        video_data["tag"] = results['tag']
        video_data['url'] = results['url']
        video_data['dirName'] = results['dir_name']
        video_data['actress'] = results['actress']
        if os.path.exists(f"jableTV/{dirName}"):
            with open(f"jableTV/{dirName}/{dirName}.json", 'w', encoding='utf-8') as f:
                f.write(json.dumps(video_data, ensure_ascii=False))
            print('json檔下載完成')
        else:
            os.mkdir(f'jableTV/{dirName}')
            with open(f"jableTV/{dirName}/{dirName}.json", 'w', encoding='utf-8') as f:
                f.write(json.dumps(video_data, ensure_ascii=False))
            print('json檔下載完成')
    except:
        print('json下載失敗')


if __name__ == "__main__":
    dirName = 'xvsr-574'
    # check_url = 'https://jable.tv/videos/ipx-907/'
    results = get_mysql_data(dirName)
    print(results)
    storge_json(results)
