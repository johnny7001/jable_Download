# 基本介紹
抓取  影片網站(jable)<br>
輕鬆爬取影片, 不用在關鍵時刻忍受lag的煩惱  

# 參考來源  
https://github.com/hcjohn463/JableTVDownload

# 資料庫結構設計  
* 抓取影片相關資訊
table_name = jableTV   

![image](https://github.com/johnny7001/crawler-comic-yomh/blob/ca954ec03d815b1a0422872b0b7e8b5adfa8a06c/yomh.jpg)

# 腳本說明  

注意: 這個code運行必須先啟動 jableAPI (https://github.com/johnny7001/jable_API/tree/master)  

check_all_status.py 確認影片下載狀態<br>
download_8s.py 下載預覽8秒短片<br>
get_json.py 將資料統整後載成json文件檔<br>
get_url_data.py 下載影片鏈結及相關資訊<br>
main.py 根據影片狀態(status)及下載清單(url_list)下載影片<br>
