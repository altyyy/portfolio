import mysql.connector
def get_db_connection():
    conn = mysql.connector.connect(
                user='root',
                password='Arutosato1021',
                host='localhost',
                database='scraping'
            )
    return conn