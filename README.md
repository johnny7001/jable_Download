# 基本介紹
抓取  影片網站(jable)<br>
輕鬆爬取影片, 不用在關鍵時刻忍受lag的煩惱  
另外抓到m3u8或mp4的url也可使用download_m3u8.py, download_mp4.py下載影片  
(成功爬取69VJ, XNXX網站影片)
# 資料庫結構設計  
* 抓取影片相關資訊
table_name = jableTV   

![image](https://github.com/johnny7001/jable_Download/blob/90a41f9d8d8a34802769b0c964d5c7105498d51b/jable.jpg)

# 腳本說明  

注意: 這個code運行必須先啟動 jableAPI (https://github.com/johnny7001/jable_API/tree/master)  

check_all_status.py 確認影片下載狀態<br>
download_8s.py 下載預覽8秒短片<br>
get_json.py 將資料統整後載成json文件檔<br>
get_url_data.py 下載影片鏈結及相關資訊<br>
main.py 根據影片狀態(status)及下載清單(url_list)下載影片<br>


# 參考來源  
https://github.com/hcjohn463/JableTVDownload
