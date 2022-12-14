# author: hcjohn463
# !/usr/bin/env python
# coding: utf-8

import requests
import os
import re
import urllib.request
import m3u8
from Crypto.Cipher import AES
from config import headers
from crawler import prepareCrawl
from merge import mergeMp4
from delete import deleteM3u8, deleteMp4
from cover import get_cover
import time
import cloudscraper
from args import *
from multiprocessing import Pool
from download_8s import get_mysql
from download_8s import main_8s
from get_json import get_mysql_data
from get_json import storge_json
from check_all_status import get_status
import ssl
from DB.jableDB import DB
import logging
import datetime

db = DB()

ssl._create_default_https_context = ssl._create_unverified_context

# 要抓取的 影片status
status_number = 3
logging.basicConfig(
    filename='video_number/jable_video.log', level=logging.INFO)
# logging.basicConfig(filename='myapp.log', level=logging.INFO)
logging.info('start'+str(datetime.datetime.now()))

# 下載影片功能


def download(url, dirName):
    folderPath = os.path.join(os.getcwd(), 'jableTV/' + dirName)
    # In[4]:
    print('正在下載', dirName)
    print(url)

    # 得到 m3u8 網址
    # response = cloudscraper.create_scraper(browser=header, delay=10).get(url=self.URL, proxies=requests_dict['googleProxy']).text
    htmlfile = cloudscraper.create_scraper(
        browser='chrome', delay=10).get(url)

    result = re.search("https://.+m3u8", htmlfile.text)
    m3u8url = result[0]

    m3u8urlList = m3u8url.split('/')
    m3u8urlList.pop(-1)
    downloadurl = '/'.join(m3u8urlList)

    # 儲存 m3u8 file 至資料夾
    m3u8file = os.path.join(folderPath, dirName + '.m3u8')
    urllib.request.urlretrieve(m3u8url, m3u8file)

    # 得到 m3u8 file裡的 URI和 IV
    m3u8obj = m3u8.load(m3u8file)
    m3u8uri = ''
    m3u8iv = ''

    for key in m3u8obj.keys:
        if key:
            m3u8uri = key.uri
            m3u8iv = key.iv

    # 儲存 ts網址 in tsList
    tsList = []
    for seg in m3u8obj.segments:
        tsUrl = downloadurl + '/' + seg.uri
        tsList.append(tsUrl)

    # 有加密
    if m3u8uri:
        m3u8keyurl = downloadurl + '/' + m3u8uri  # 得到 key 的網址

        # 得到 key的內容
        response = requests.get(m3u8keyurl, headers=headers, timeout=10)
        contentKey = response.content

        vt = m3u8iv.replace("0x", "")[:16].encode()  # IV取前16位

        ci = AES.new(contentKey, AES.MODE_CBC, vt)  # 建構解碼器
    else:
        ci = ''

    # 刪除m3u8 file
    deleteM3u8(folderPath)

    # 開始爬蟲並下載mp4片段至資料夾
    prepareCrawl(ci, folderPath, tsList)

    # 合成mp4
    mergeMp4(folderPath, tsList)

    # 刪除子mp4
    deleteMp4(folderPath)

    # get cover
    get_cover(html_file=htmlfile, folder_path=folderPath)


# 要爬取的網址清單
url_list = []

parser = get_parser()
args = parser.parse_args()

if (len(args.url) != 0):
    url = args.url
elif (args.random == True):
    url = av_recommand()
else:
    content = get_status(status_number)
    content_list = content.split(',')
    for url in content_list:
        url_list.append(url.replace(
            '[', '').replace(']', '').replace("'", '').strip())
# print(url_list)
# -------------------------------------------------------------------------------------------
main_list = []
main_list = url_list[:4]
# print(main_list)
# 主程式


def main(url):
    urlSplit = url.split('/')
    dirName = urlSplit[-2]
    # print(dirName)
    # 獲得網址, 將status 改成1
    try:
        sql = f"UPDATE `jable01_tv` SET `status`= 1 WHERE `dir_name` = '{dirName}';"
        db.query(sql)

        # 若資料夾不存在則創立
        if not os.path.exists('jableTV/' + dirName):
            os.makedirs('jableTV/' + dirName)
        # 資料夾存在但資料夾裡面沒有番號mp4檔，表示下載失敗
        elif not os.path.isfile(f'jableTV/{dirName}/{dirName}.mp4'):
            # 將資料夾內原本失敗的清空, 重新下載
            download(url, dirName)  # 影片下載
            print(f'下載{dirName}的影片')
        if not os.path.isfile(f'jableTV/{dirName}/{dirName}_8s.mp4'):
            print(f'下載{dirName}的8秒短片')
            short_url = get_mysql(url)
            main_8s(dirName, short_url)  # 8秒短片下載
        if not os.path.isfile(f'jableTV/{dirName}/{dirName}.json'):
            print(url)
            print(f'下載{dirName}的json檔')
            results = get_mysql_data(url)
            storge_json(results)
        # 獲得網址, 將status 改成2
        sql = f"UPDATE `jable01_tv` SET `status`= 2 WHERE `dir_name` = '{dirName}';"
        db.query(sql)
    except Exception as e:
        logging.info(f'{dirName}下載失敗')
        logging.info(e)


if __name__ == '__main__':  # 多進程測試，參考網站：https://zhuanlan.zhihu.com/p/335831949
    start_4 = time.time()
    pool = Pool(processes=4)
    pool.map(main, main_list)
    end_4 = time.time()
    print('4個進程', end_4 - start_4)
    pool.terminate()  # terminate() 通常在主程序的可並行化部分完成時調用。
    pool.join()  # 調用 join() 以等待工作進程終止。
