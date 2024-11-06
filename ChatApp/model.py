import pymysql  # type: ignore
from flask import abort
import os
from util.DB import DB

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

    @staticmethod
    def getChannelName(channel_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE name=%s;"
            cur.execute(sql, (channel_name))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()

    @staticmethod
    def addChannel(user_id,channel_name, channel_description):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (user_id, name, description) VALUES (%s, %s, %s);"
            cur.execute(sql, (user_id, channel_name, channel_description))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()
        