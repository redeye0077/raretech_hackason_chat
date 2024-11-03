from ast import Return
from flask import Flask, render_template, request, redirect, url_for, make_response  # type: ignore

import os
from model import PostModel  # model.pyをインポート
from DB import DB

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 新規登録画面
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # 入力データをデータベースに挿入
        PostModel.insert_user(name,email, password)
        # Cookieに保存
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('last_post', email)
        return resp

    return render_template('signup.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)