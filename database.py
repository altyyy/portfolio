import mysql.connector


# DBへ接続
conn = mysql.connector.connect(
    user='root',
    password='Arutosato1021',
    host='localhost',
    database='scraping'
)

# DBの接続確認
if not conn.is_connected():
    raise Exception("MySQLサーバへの接続に失敗しました")

# カーソルを作成
cursor = conn.cursor()

# 挿入するデータ（例）
title = "hoge"
access = "hogee"
age = "hogeeee"

# INSERTクエリ
insert_query = """
INSERT INTO houses  (title,access,age)
VALUES (%s,%s,%s)
"""

# データのタプル
data = (title, access, age)

# クエリの実行
cursor.execute(insert_query, data)

# 変更をコミット
conn.commit()

# 挿入したレコード数の表示
print(cursor.rowcount, "record(s) inserted")

# カーソルと接続を閉じる
cursor.close()
conn.close()