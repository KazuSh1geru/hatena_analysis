#%%
import pandas as pd

from datetime import datetime

import matplotlib.pyplot as plt
# import matplotlib as mpl

# 日本語フォントの設定
# mpl.rcParams['font.family'] = 'IPAGothic'
#%%
# DFの読み込み
data_path = "../output/csv/hatebu_20230222.csv"
df = pd.read_csv(data_path)
df.info()
#%%
df.describe()
#%%
format = "%Y-%m-%d %H:%M:%S"

published_list = df.published.to_list()
published_hour_list = list(
            map(lambda x:datetime.strptime(x, format).hour, published_list)
        )

plt.hist(published_hour_list, bins=12)
plt.xlabel('publised_hour')
plt.ylabel('count')
plt.title('')
plt.show()

#%%
published_term_list = ["beforenoon" if x <= 12 else "afternoon" for x in published_hour_list]

plt.hist(published_term_list, bins=2)
plt.xlabel('publised_hour')
plt.ylabel('count')
plt.title('')
plt.show()
#%%
plt.hist(df.bookmark_num.to_list()
    , bins=50
    ,log=True
)
plt.xlabel('bookmark')
plt.ylabel('count')
plt.title('')
plt.show()

# %%
# 外れ値っぽい２つを削除してみる
bookmark_list = df.bookmark_num.to_list()

for _ in range(2):
    max_value = max(bookmark_list)
    bookmark_list.remove(max_value)
    
plt.hist(bookmark_list
         , bins=50
        #  ,log=True
         )
plt.xlabel('bookmark')
plt.ylabel('count')
plt.title('')
plt.show()

# %%
x = published_hour_list
y = df.bookmark_num.to_list()

# グラフの描画
plt.scatter(x, y)
plt.title('relation between publised_hour and bookmark')
plt.show()
# %%
