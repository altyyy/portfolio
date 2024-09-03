from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import datetime
import mysql.connector
import re
from config import get_db_connection

##数字だけ取り出す関数
def extract_numbers(text):
    pattern = r'\d+(?:\.\d+)?'
    numbers = re.findall(pattern, text)
    return ''.join(numbers)

##連続した数字を一つずつ格納する
def extract_numbers2(string):
    # 連続した数字のシーケンスを取り出す
    numbers = re.findall(r'\d+', string)
    return numbers

#一番小さい数を取ってくる
def find_smallest_number(numbers):
    # 数字のリストを整数に変換し、最小の数を見つける
    int_numbers = [int(num) for num in numbers]
    smallest_number = min(int_numbers)
    return smallest_number

#築年数
def check_new_or_age(string):
    if "新築" in string:
        return 0
    else:
        # "築"と"年"の間の数字を取り出す
        match = re.search(r'築(\d+)年', string)
        if match:
            return int(match.group(1))
        else:
            return None  # 数字が見つからなかった場合

# 複数の変数を一括で空白の場合nullに変える処理
def replace_blank_with_none(input_string):
    if input_string is None or not input_string.strip():
        return None
    return input_string

def update_variables(*var_names):
    for name in var_names:
        globals()[name] = replace_blank_with_none(globals()[name])



# 変数urlにSUUMOホームページのURLを格納する
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&ek=024041310&rn=0240&page={}'
r = requests.get(url)
# print(r.status_code)
# 変数d_listに空のリストを作成する
d_list = []

# アクセスするためのURLをtarget_urlに格納する
i = 1
while True:
    print(i)
    target_url = url.format(i)

    # target_urlへのアクセス結果を、変数rに格納
    r = requests.get(target_url)
    sleep(1)

    # 取得結果を解析してsoupに格納
    soup = BeautifulSoup(r.text)
    
    # すべての物件情報(20件)を取得する
    contents = soup.find_all('div', class_='cassetteitem')

    # 各物件情報をforループで取得する
    for content in contents:
        # 物件情報と部屋情報を取得しておく
        detail = content.find('div', class_='cassetteitem_content')
        table = content.find('table', class_='cassetteitem_other')

        # 物件情報から必要な情報を取得する
        title = detail.find('div', class_='cassetteitem_content-title').text
        address = detail.find('li', class_='cassetteitem_detail-col1').text
        access = detail.find('li', class_='cassetteitem_detail-col2').text
        age = detail.find('li', class_='cassetteitem_detail-col3').text

        #した二つの変数にリストで保持されているからインサートできない　accessは一番小さい数　ageは築年数の間だけ
        access = extract_numbers2(access)
        access = find_smallest_number(access)
        age = check_new_or_age(age)

        # 部屋情報のブロックから、各部屋情報を取得する
        tr_tags = table.find_all('tr', class_='js-cassette_link')

        # 各部屋情報をforループで取得する
        for tr_tag in tr_tags:

            # 部屋情報の行から、欲しい情報を取得する
            floor, price, first_fee, capacity = tr_tag.find_all('td')[2:6]

            # さらに細かい情報を取得する
            fee, management_fee = price.find_all('li')
            deposit, gratuity = first_fee.find_all('li')
            madori, menseki = capacity.find_all('li')

            floor = extract_numbers(floor.text)
            fee = extract_numbers(fee.text)
            management_fee = extract_numbers(management_fee.text)
            deposit = extract_numbers(deposit.text)
            gratuity = extract_numbers(gratuity.text)
            menseki = extract_numbers(menseki.text)

            update_variables("floor","fee","management_fee","deposit","gratuity","menseki")



            #データベース接続
            conn = get_db_connection()
            
            # DBの接続確認
            if not conn.is_connected():
                raise Exception("MySQLサーバへの接続に失敗しました")

            # カーソルを作成
            cursor = conn.cursor()


            # INSERTクエリ
            insert_query = """
            INSERT INTO houses  (title,address,access,age,floor,fee,management_fee,deposit,madori,gratuity,menseki)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """


            # データのタプル
            data = (title,address,access,age,floor,fee,management_fee,deposit,madori.text,gratuity,menseki)


            # クエリの実行
            cursor.execute(insert_query, data)

            # 変更をコミット
            conn.commit()

            # 挿入したレコード数の表示
            print(cursor.rowcount, "record(s) inserted")

            # カーソルと接続を閉じる
            cursor.close()
            conn.close()
            
　 　i += 1
