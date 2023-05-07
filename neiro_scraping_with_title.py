# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:54:09 2023

@author: naoya
"""

#参考サイト
"""
beautifulsoup
https://ai-inter1.com/beautifulsoup_1/
問題解決
https://teratail.com/questions/180585
"""
###########################################################サイトごとに変更するサイン

#ライブラリのインポート
from bs4 import BeautifulSoup
import requests
import csv
import textwrap
import re

#urlの指定
url = input("csvファイルに書き出したいサイトのURLを入力してください:")
#csvファイルの指定
csv_file = input("csvファイルの名前を入力してください(.csvは不要):") + ".csv"
#ボイスの種類数の指定
voice = 4
#ボイスの名前を指定
voice_0 = "赤"
voice_1 = "青"
voice_2 = "黒"
voice_3 = "緑" 

def color_select(count,date):#どのゆっくりボイスに話させるか分ける(voice追加時はここを変更)
    if count%voice == 0:
        date["color"] = "赤"
        return date
    elif count%voice == 1:
        date["color"] = "青"
        return date
    elif count%voice == 2:
        date["color"] = "黒"
        return date
    elif count%voice == 3:
        date["color"] = "緑"
        return date
    
"""追加時のテンプレ
    elif count%voice == :
        date = dict(color="")
        return date
"""
def remove_quotes(text):
    # 先頭にある">>"を取り除く
    text = re.sub(r'^>>\d+\s*', '', text)
    
    # 先頭にある全角の数字とスペースの後に続く">>"を取り除く
    text = re.sub(r'^>>[\uff10-\uff19]+\s*', '', text)
    
    return text

#urlからwebページを取得
r = requests.get(url)
#print(r.content)

#webページを分析
soup = BeautifulSoup(r.content, 'html.parser')

#######################################サイトごとに変わる可能性あり############################

#titleを取得
title = soup.select("#container > div.main-container > div > article > header > h1 > a")
#titleを表示
t = str(soup.article.header.h1.a.string)
print(f"タイトルはこちらです:{soup.article.header.h1.a.string}")

########################################################################################



#辞書を格納するlist
whole_date = []
ti = "今回は 「"+t+"」\nに対する読者の反応を紹介します"
if "【ワンピース】" in ti:
    ti = ti.replace("【ワンピース】", "")
ti = textwrap.fill(ti,25)
soredeha = "それではどうぞ"
title_content = {"color":"タイトル","content":ti}
whole_date.append(title_content)
sore = {"color":"タイトル","content":soredeha}
whole_date.append(sore)


date = {"content":""}#各レスを色とともに格納する辞書


b = ""#contentの中身
count = 0
for i in soup.select("div.t_h b"):############################################
    res = i.text
    res = res.strip()
    if res == None:
        continue
    elif res.startswith(">>"):
        res = remove_quotes(res)
        b += res
        color_select(count,date)
    else:
        print(res)
        b += res
        color_select(count,date)

    b = b.replace('\u3000', '')#全角スペースなどに対処
    b = b.replace('\u200b', '')
    
    #両端の空白を削除
    b = b.strip()
    
    b = textwrap.fill(b,25)
    
    date["content"] = b
    #print(b)
    b = ""#スレ内容のリセット

    if date["content"] != "":#中身が無いものを除外
        whole_date.append(date)
    else: continue

    date = {}#レスごとに辞書を作成(初期化)
    count += 1
  
#print(whole_date)
path = 'C:\\Users\\naoya\\OneDrive\\デスクトップ'
csv_file = path + "/" + csv_file
    
#csvに書き出し
try:
    with open(csv_file,"w",newline="",encoding = 'utf_8') as f:
        fieldnames = ["color","content"]
        dict_writer = csv.DictWriter(f,fieldnames = fieldnames)
        
        dict_writer.writerows(whole_date)
        
except FileNotFoundError as e:
    print("---------------------------")
    print(e)
    print("---------------------------")
except csv.Error as e:
    print("---------------------------")
    print(e)
    print("---------------------------")
except UnicodeEncodeError as e:
    print("---------------------------")
    print(e)
    print("---------------------------")
