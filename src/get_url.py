import requests
from bs4 import BeautifulSoup

# ブログ記事一覧ページのURLを指定する
TARGET_ACCOUNT_URL = 'https://link-and-motivation.hatenablog.com'
url = f'{TARGET_ACCOUNT_URL}/archive'

# ページのHTMLを取得する
response = requests.get(url)

# HTMLをパースする
soup = BeautifulSoup(response.content, 'html.parser')

# 記事のURLを抽出する
entry_urls = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.startswith(f'{TARGET_ACCOUNT_URL}/entry/'):
        entry_urls.append(href)

# 結果を出力する
for entry_url in entry_urls:
    print(entry_url)
