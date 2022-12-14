import pymysql
import requests


def get_status(status_number):
    url = f'http://127.0.0.1:3123/status/{status_number}'
    r = requests.post(url)
    result = r.text
    return result


if __name__ == "__main__":
    url_list = []
    content = get_status(2)  # content type = str
    content_list = content.split(',')

    for url in content_list:
        url_list.append(url.replace(
            '[', '').replace(']', '').replace("'", '').strip())
    print(url_list)
