from ast import Return
from flask import Flask, flash, render_template, request, redirect, session, url_for, make_response  # type: ignore

import os
from model import PostModel  # model.pyをインポート
from util.DB import DB

app = Flask(__name__)
app.debug = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    
    # フォームが空かどうかをチェック
    if not email:
        flash('空のフォームがあるようです')
        return redirect('/login')
    
    # メールアドレスに対応するユーザーの取得
    user = PostModel.getUser(email)
    
    # ユーザーが見つからない場合のエラー処理
    if not user:
        flash('ユーザーが見つかりません。正しいメールアドレスを入力してください。')
        return redirect('/login')
    
    # ユーザーが見つかり、セッションにユーザーIDを設定
    session['user_id'] = user["id"]
    return redirect('/index')

# 部屋一覧画面
@app.route('/index')
def index():
    channels = PostModel.getChannel()
    return render_template('index.html', channels=channels)

#サインアウト処理
@app.route('/signout', methods=['POST'])
def signout():
    session.clear()
    return redirect('/login')

# 削除画面に遷移
@app.route('/channel_delete/<int:channel_id>')
def channel(channel_id):
    # データベースから該当のチャンネルを取得
    channel = PostModel.getChannelId(channel_id)
    if channel:
        return render_template('edit-channel/delete-channel.html',channel=channel)
    else:
        return "チャンネルが見つかりませんでした。", 404

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

# 部屋追加画面
@app.route('/channel_add')
def channelAddIndex():
    return render_template('edit-channel/add-channel.html')

# 部屋追加処理
@app.route('/channel_add',methods=['POST'])
def channelAdd():
    user_id = session.get("user_id")
    # フォームからチャンネル名と説明を取得
    channel_name = request.form.get('channel_name')
    channel_description = request.form.get('channel_description')
    # チャンネル名が空の場合のチェック
    if not channel_name or not channel_description:
        error = '空のフォームがあるようです'
        return render_template('edit-channel/add-channel.html', error_message_brank=error)
    # チャンネル名の重複チェック
    existing_channel = PostModel.getChannelName(channel_name)
    if existing_channel:
        error = '既に同じ名前のチャンネルが存在しています！'
        return render_template('edit-channel/add-channel.html', error_message_duplication=error)
    # チャンネル追加
    else:
        PostModel.addChannel(user_id,channel_name, channel_description)
        flash('部屋を追加しました！')
    return redirect(url_for('channelAddIndex'))

# 部屋削除処理
@app.route('/channel_delete/<int:channel_id>/delete',methods=['POST'])
def deleteChannel(channel_id):
    user_id = session.get("user_id")
    channel = PostModel.getChannelId(channel_id)
    #部屋作成者以外削除できないようにする
    if channel["user_id"] != user_id:
        error = '部屋は作成者のみ削除可能です'
        return render_template('edit-channel/delete-channel.html', channel=channel, error_message=error)
    #部屋削除
    PostModel.deleteChannel(channel_id)
    flash('部屋を削除しました')
    return redirect(url_for('index'))

# テスト
@app.route('/test')
def test():
    pagetitle = "hogehoge部屋"

    return render_template('edit-channel/test.html' , pagetitle = pagetitle)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
