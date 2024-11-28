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


    def getUser(email):
        try:
            conn = DB.getConnection()
            if conn is None:
                return None
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email))
                user = cur.fetchone()
                return user
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def getUserByName(name):
        try:
            conn = DB.getConnection()
            if conn is None:
                return None
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE name = %s;"
                cur.execute(sql, (name))
                user = cur.fetchone()
                return user
        except pymysql.MySQLError as e:
            print(f'エラーが発生しています：{e}')
            return None
        finally:
            if conn:
                conn.close()

    def getChannel():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT id, name, description FROM channels;"
            cur.execute(sql)
            channels = cur.fetchall()
            return channels
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()

    @staticmethod
    def getChannelId(channel_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT id, user_id, name, description FROM channels WHERE id = %s;"
            cur.execute(sql, (channel_id))
            channels = cur.fetchone()
            return channels
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()

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

    def deleteChannel(channel_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM channels WHERE id=%s;"
            cur.execute(sql, (channel_id))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()

    def getMessage(channel_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT me.id AS message_id, us.id AS user_id, us.name AS name, content, me.created_at AS created_at FROM messages AS me INNER JOIN users AS us ON me.user_id = us.id WHERE me.channel_id = %s ORDER BY me.created_at ASC;"
            cur.execute(sql, (channel_id))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()

    def createMessage(user_id, channel_id, content, created_at):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(user_id, channel_id, content, created_at) VALUES(%s, %s, %s, %s)"
            cur.execute(sql, (user_id, channel_id, content, created_at))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()
        

