import pymysql  # type: ignore

class DB:
    @staticmethod
    def getConnection():
        try:
            conn = pymysql.connect(
                host="db",  # ホスト名
                db="flaskapp",  # 使用するデータベース名
                user="root",  # ユーザー名
                password="password",  # パスワード
                charset="utf8",  # 文字セット
                cursorclass=pymysql.cursors.DictCursor  # 結果を辞書形式で取得
            )
            return conn
        except pymysql.MySQLError as e:
            print(f"コネクションエラーです: {e}")
            return None  # 接続できなかった場合はNoneを返す
