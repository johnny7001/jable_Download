import requests
import m3u8
import time

m3u8Url = 'http://www.***********.m3u8'
header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


def download_m3u8_video(m3u8Url, save_name):  # 下載影片, 檔名

    playlist = m3u8.load(urL=m3u8Url, headers=header)
    # n = len(playlist.segments)
    size = 0
    start = time.time()

    for i, seg in enumerate(playlist.segments, 1):
        r = requests.get(seg.absolute_uri, headers=header)
        data = r.content
        size += len(data)
        with open(save_name, "ab" if i != 1 else "wb") as f:
            f.write(data)
    end = time.time()

    print('下載完成，共花費'+str(end-start))
