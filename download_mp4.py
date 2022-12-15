import requests
import time
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
video_url = 'http://www.***********.mp4'
video_url_name = '影片名稱'
downsize = 0
print('開始下載')
startTime = time.time()
req = requests.get(video_url, headers=headers, stream=True, verify=False)
with (open(video_url_name+'.mp4', 'wb')) as f:
    for chunk in req.iter_content(chunk_size=10000):
        if chunk:
            f.write(chunk)
            downsize += len(chunk)
            line = 'downloading %d KB/s - %.2f MB， 共 %.2f MB'
            line = line % (
                downsize / 1024 / (time.time() - startTime), downsize / 1024 / 1024, downsize / 1024 / 1024)
            print(line)
