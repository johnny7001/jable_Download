# JableTVDownload

## 下載JableTV好幫手

每次看正要爽的時候就給我卡住轉圈圈  

直接下載到電腦看沒煩惱

### vitual env
```
python3 -m venv jable
source jable/bin/activate. # MacOS
```

### requirements
`pip install -r requirements.txt`

安裝 [FFmpeg] (未安裝也能下載 但影片拖拉時間軸會有卡幀情況發生)

### 執行程式(Execute)
`python main.py`

### 輸入影片網址(Input video url)
`https://jable.tv/videos/ipx-486/`    
![image](https://github.com/hcjohn463/JableDownload/blob/main/img/input.PNG)  

### 等待下載(Wait download)  
![image](https://github.com/hcjohn463/JableDownload/blob/main/img/download.PNG)

### 完成(Finish)
![image](https://github.com/hcjohn463/JableDownload/blob/main/img/3.PNG)

如果覺得好用 再麻煩給個星星好評 謝謝!!

## #####選擇性使用(Optional use)#####

### 使用FFmpeg轉檔優化 : 參數能自己調(Use FFmpeg encode) 
`cd ipx-486`  
`ffmpeg -i ipx-486.mp4 -c:v libx264 -b:v 3M -threads 5 -preset superfast f_ipx-486.mp4`  
  
![image](https://github.com/hcjohn463/JableDownload/blob/main/img/ff.PNG)

### 轉檔完成(Finish encode)
![image](https://github.com/hcjohn463/JableDownload/blob/main/img/different.PNG)

[FFmpeg]:<https://www.ffmpeg.org/>  

### Argument parser
`$python main.py -h`

![](https://i.imgur.com/qgyS5sf.png)

`$python main.py --random True`

可以直接下載隨機熱門影片

![](https://i.imgur.com/dSsdB7Y.png)

可以直接在cmd line指定url。

![](https://i.imgur.com/DKFrD7T.png)

