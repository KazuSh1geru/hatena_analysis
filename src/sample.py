from bs4 import BeautifulSoup
from requests import get
from time import sleep
from pprint import pprint
from time import sleep
import os

from dateutil import parser
from datetime import datetime

import csv

# リクエスト間隔を指定(秒)　※サーバに負荷をかけないよう3秒以上を推奨
INTERVAL = 3
# はてブデータを格納するCSVファイルの保存先を指定
HATEBU_FILE_DIR = "./output/hatebu/csv/"
# はてブデータを格納するCSVファイルの名前を指定
date = datetime.today().strftime('%Y%m%d')
HATEBU_FILE_NAME = f"hatebu_{date}.csv"

HATEBU_FILE_HEADER = "code,title,bookmark_num,published\n"

# URLの固定部分を指定
# FIXED_URL = "https://link-and-motivation.hatenablog.com/entry/"

target_url_list = [
    "https://link-and-motivation.hatenablog.com/entry/2022/12/28/094219",
    "https://link-and-motivation.hatenablog.com/entry/2022/12/26/121837"
]

os.makedirs(HATEBU_FILE_DIR, exist_ok=True)
with open(HATEBU_FILE_DIR + HATEBU_FILE_NAME, "w", encoding="shift_jis") as csv_file:
    csv_file.write(HATEBU_FILE_HEADER)

if __name__ == "__main__":
    
    for target_url in target_url_list:
        html = get(target_url)
        soup = BeautifulSoup(html.content, 'html.parser')
        
        # 記事タイトルの取得
        blog_request = get(f"http://hatenablog.com/oembed?url={target_url}")
        blog_json = blog_request.json()
        # pprint(blog_json)
        title = blog_json["title"]
        published = blog_json["published"]
        
        # bookmark数の取得 -> 公式APIを使用する
        bookmark = get(f"https://bookmark.hatenaapis.com/count/entry?url={target_url}")
        bookmark_number = bookmark.text
        
        # # CSVデータを格納する変数を定義
        article_code = 121837
        csv_text = str(article_code)

        # データにコロンを付けて変数に格納
        csv_text += "," + title + "," + bookmark_number + "," + published
        print(csv_text)
        
        with open(HATEBU_FILE_DIR + HATEBU_FILE_NAME, "a", encoding="shift_jis") as csv_file:
            csv_file.write(csv_text + "\n")
        
        # 時間おく
        sleep(INTERVAL)