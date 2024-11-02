import pymysql  # type: ignore
import os
from DB import DB

   

class PostModel:
    @staticmethod
    def insert_user(email, password):
        conn = DB.getConnection()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO posts (email, password) VALUES (%s, %s)', (email, password))
            conn.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"ユーザーの挿入エラーです: {e}")
            return False
        finally:
            conn.close()
