import requests
from bs4 import BeautifulSoup
import json
import os

# ブログ記事一覧ページのURLを指定する
TARGET_ACCOUNT_URL = 'https://link-and-motivation.hatenablog.com'

url = f'{TARGET_ACCOUNT_URL}/archive'

# 記事のURLを格納するリスト
entry_urls = []
# ページネーションがある場合のループ処理
URL_FILE_DIR = "./output/url/"
os.makedirs(URL_FILE_DIR, exist_ok=True)

while True:
    # ページのHTMLを取得する
    response = requests.get(url)

    # HTMLをパースする
    soup = BeautifulSoup(response.content, 'html.parser')

    # 記事のURLを抽出する
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith(f'{TARGET_ACCOUNT_URL}/entry/'):
            entry_urls.append(href)

    # 次のページがある場合、ページネーションのリンクを取得する
    next_page_link = soup.find('a', {'class': 'next'})

    # 次のページがない場合は処理を終了する
    if not next_page_link:
        break

    # 次のページのURLを取得する
    next_page_url = next_page_link.get('href')

    # 次のページのURLが相対パスの場合、絶対パスに変換する
    if not next_page_url.startswith('http'):
        next_page_url = TARGET_ACCOUNT_URL + next_page_url

    # 次のページのURLに移動する
    url = next_page_url

# 結果を出力する
for entry_url in entry_urls:
    print(entry_url)
    
with open(f'{URL_FILE_DIR}/blog_url.json', 'w') as f:
    json.dump(entry_urls, f, indent=2)