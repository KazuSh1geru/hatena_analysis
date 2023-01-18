from bs4 import BeautifulSoup
from requests import get
from time import sleep
import os
import csv

# はてブデータを格納するCSVファイルの保存先を指定
HATEBU_FILE_DIR = "./output/hatebu/csv/"

# はてブデータを格納するCSVファイルの名前を指定
HATEBU_FILE_NAME = "test_20230118.csv"

HATEBU_FILE_HEADER = "article_code,title,bookmark_num\n"

# URLの固定部分を指定
# FIXED_URL = "https://link-and-motivation.hatenablog.com/entry/"

target_url_list = [
    "https://link-and-motivation.hatenablog.com/entry/2022/12/28/094219",
    "https://link-and-motivation.hatenablog.com/entry/2022/12/26/121837"
]

if __name__ == "__main__":
    
    for target_url in target_url_list:
        html = get(target_url)
        soup = BeautifulSoup(html.content, 'html.parser')
        
        # 記事タイトルの取得
        hatebu_titles = soup.find_all("h1")
        # コミュニティタイトル, 記事タイトルは二番目
        hatebu_title = hatebu_titles[1]
        hatebu_title_element = hatebu_title.select("a")
        # print(hatebu_title_element)
        title = hatebu_title_element[0].text
        # print(title)
        
        # bookmark数の取得 -> 公式APIを使用する
        bookmark = get(f"https://bookmark.hatenaapis.com/count/entry?url={target_url}")
        bookmark_number = bookmark.text
        
        # # CSVデータを格納する変数を定義
        article_code = 121837
        csv_text = str(article_code)

        # # オッズデータにコロンを付けて変数に格納
        csv_text += "," + title + "," + bookmark_number
        print(csv_text)