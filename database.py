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

cur = conn.cursor(dictionary=True)  # 取得結果を辞書型で扱う設定

query__for_fetching = """
SELECT
    houses.id   AS id,
    houses.title AS title
FROM houses
ORDER BY houses.id
;
"""

cur.execute(query__for_fetching)

for fetched_line in cur.fetchall():
    id = fetched_line['id']
    name = fetched_line['title']
    print(f'{id}: {name}')