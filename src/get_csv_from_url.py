from requests import get
from time import sleep
import os

from datetime import datetime
import json
from urllib.parse import urlparse

# リクエスト間隔を指定(秒)　※サーバに負荷をかけないよう3秒以上を推奨
INTERVAL = 3
# はてブデータを格納するCSVファイルの保存先を指定
HATEBU_FILE_DIR = "./output/csv/"
# はてブデータを格納するCSVファイルの名前を指定
create_date = datetime.today().strftime('%Y%m%d')
HATEBU_FILE_NAME = f"hatebu_{create_date}.csv"

HATEBU_FILE_HEADER = "entry_code,title,bookmark_num,published,categories,url\n"

# URLの固定部分を指定
# FIXED_URL = "https://link-and-motivation.hatenablog.com/entry/"

with open('./output/url/blog_url.json', 'r') as f:
    target_url_list = json.load(f)
# target_url_list = ["https://link-and-motivation.hatenablog.com/entry/four-keys-metrics-dashboard"]

os.makedirs(HATEBU_FILE_DIR, exist_ok=True)
with open(HATEBU_FILE_DIR + HATEBU_FILE_NAME, "w", encoding="shift_jis") as csv_file:
    csv_file.write(HATEBU_FILE_HEADER)

if __name__ == "__main__":
    
    for target_url in target_url_list:
        # 記事タイトルの取得
        blog_request = get(f"http://hatenablog.com/oembed?url={target_url}")
        blog_json = blog_request.json()
        title = blog_json["title"]
        published = blog_json["published"]
        categories = ','.join(blog_json["categories"])  # categoriesがリストなので文字列に変換
        
        # bookmark数の取得 -> 公式APIを使用する
        bookmark = get(f"https://bookmark.hatenaapis.com/count/entry?url={target_url}")
        bookmark_number = bookmark.text
        
        # 記事のentry以下を取得する
        parsed_url = urlparse(target_url)
        element_list = parsed_url.path.split('/')
        # listからentryを見つける
        entry_index = element_list.index("entry")
        article_code = '/'.join(element_list[entry_index+1:])
        
        csv_text = str(article_code)

        # データにコロンを付けて変数に格納
        csv_text += "," + title + "," + bookmark_number + "," + published + "," + categories + "," + target_url 
        print(csv_text)
        
        with open(HATEBU_FILE_DIR + HATEBU_FILE_NAME, "a") as csv_file:
            csv_file.write(csv_text + "\n")
        
        # 時間おく
        sleep(INTERVAL)