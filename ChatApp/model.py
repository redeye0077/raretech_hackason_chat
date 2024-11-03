import pymysql  # type: ignore
import os
from DB import DB

   

class PostModel:
    @staticmethod
    def insert_user(name, email, password):
        login_count = 0
        conn = DB.getConnection()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO users (name, email, password, login_count) VALUES (%s, %s ,%s, %s)', (name, email, password, login_count))
            conn.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"ユーザーの挿入エラーです: {e}")
            return False
        finally:
            conn.close()
