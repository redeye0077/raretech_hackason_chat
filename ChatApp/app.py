from ast import Return
from flask import Flask, flash, render_template, request, redirect, session, url_for, make_response  # type: ignore

import os
from model import PostModel  # model.pyをインポート

app = Flask(__name__)
app.debug = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

#サインアウト処理
def signout():
    session.clear()
    return redirect('/login')

@app.route('/index', methods=['POST'])
def signoutIndex():
    return signout()

@app.route('/message', methods=['POST'])
def signoutMessage():
    return signout()

@app.route('/channel_add', methods=['POST'])
def signoutChannelAdd():
    return signout()

@app.route('/channel_delete', methods=['POST'])
def signoutChannelDelete():
    return signout()

#チャンネル追加画面
@app.route('/channel-add')
def channelAddIndex():
    return render_template('edit-channel/add-channel.html')

@app.route('/channel-add',methods=['POST'])
def channelAdd():
    user_id = 1
    # フォームからチャンネル名と説明を取得
    channel_name = request.form.get('channel_name')
    channel_description = request.form.get('channel_description')
    # チャンネル名が空の場合のチェック
    if not channel_name or not channel_description:
        error = '空のフォームがあるようです'
        return render_template('edit-channel/add-channel.html', error_message=error)
    # チャンネル名の重複チェック
    existing_channel = PostModel.getChannelName(channel_name)
    if existing_channel:
        error = '既に同じ名前のチャンネルが存在しています！'
        return render_template('edit-channel/add-channel.html', error_message=error)
    # チャンネル追加
    else:
        PostModel.addChannel(user_id,channel_name, channel_description)
        flash('部屋を追加しました！')
    return redirect(url_for('channelAddIndex'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)