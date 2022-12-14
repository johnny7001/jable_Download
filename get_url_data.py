from posixpath import dirname
from bs4 import BeautifulSoup
import pymysql
import requests
import cloudscraper
import json
import os
import pymysql
import logging
# from dotenv import load_dotenv
# load_dotenv()
# jablefile = os.getenv("file")
import datetime
from shane_db import DB

db = DB()
logging.basicConfig(filename='jableDownloadTV/myapp.log', level=logging.INFO)
# logging.basicConfig(filename='myapp.log', level=logging.INFO)
logging.info('start'+str(datetime.datetime.now()))
for x in range(1, 50):
    status = 0
    main = f"https://jable.tv/hot/{x}/"
    print(main)
    r = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }).get(main).text
    soup = BeautifulSoup(r)
    total_video_url = soup.find_all("div", class_="col-6 col-sm-4 col-lg-3")
    for video_url in total_video_url:
        # 影片網址
        url = video_url.find('a').attrs['href']
        # 8秒短片(mp4)
        short_url = video_url.find('img', {'class':'lazyload'}).get('data-preview')
        # 番號
        number = url.split('video/')[0].split('videos/')[1].split('/')[0]
        
        sql = f"select dir_name from shane.jable01_tv where dir_name = '{number}';"
        result = db.query(sql).fetchone()
        if result == None:
            sql = ""
            a = cloudscraper.create_scraper(browser={
                'browser': 'firefox',
                'platform': 'windows',
                'mobile': False
            }).get(url).text
            soup2 = BeautifulSoup(a)
            # 影片標題
            header = soup2.find('h4').text

            # print(header)
            all_tags = soup2.find('div', class_="text-center").find('h5').find_all('a')
            tags = []
            for one_tag in all_tags:
                tags.append(one_tag.text)
            # 標籤
            # print(tags)
            tags = str(tags)

            #所有演員
            actress_list = []
            # img -- data-original-title, a -- title
            all_actress = soup2.find_all('a', class_='model')
            for actress in all_actress:
                # print(actress)
                if actress.find('span'):
                    name = actress.find('span').get('title')
                    actress_list.append(name)
                elif actress.find('img'): 
                    name = actress.find('img').get('title')
                    actress_list.append(name)
            actress_list = str(actress_list)
            # print(f'影片網址: {url}, 8秒短片: {short_url}, 番號: {number}, 影片標題: {header}, 標籤: {tags}, 演員: {actress_list}')
            # print('*'*50)
            data = [header, url, short_url, tags, status, number, actress_list]
            try:
                conn = pymysql.connect(host='sgpdb.itlab.tw', port=8889, user='shane', password="GKbCoMubLMQ6o",
                            database='shane')
                cursor = conn.cursor()
                sql = "INSERT INTO `jable01_tv` (`header`, `url`, `short_url`, `tag`, `status`, `dir_name`, `actress`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, data)
                conn.commit()
                print('insert成功')
                conn.close()
            except Exception as e: 
                logging.info(f'影片網址: {url}, 8秒短片: {short_url}, 番號: {number}, 影片標題: {header}, 標籤: {tags}, 演員: {actress_list}')
                logging.info(e)
        else:
            print(f'{number}已存在於資料庫')
            