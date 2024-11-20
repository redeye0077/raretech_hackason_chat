import os
import re
import pytz
from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session
from model import PostModel  # model.pyをインポート
from ast import Return
from datetime import datetime,timezone
import hashlib
from util.DB import DB

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
app.debug = True

# 最初のページを/loginにリダイレクトする
@app.route('/')
def home():
    return redirect(url_for('login'))

# サインアップページの表示
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('registration/signup.html')

# 新規登録画面 (POSTメソッドのみ)
@app.route('/signup', methods=['POST'])
def userSignup():

    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                                 
 # フォームの入力検証
    if name == '' or email == '' or password1 == '' or password2 == '':
        error = '空のフォームがあるようです'
        return render_template('registration/signup.html', error_message1=error)
    
    if email == '':
        error = '入力されていません'
        return render_template('registration/signup.html', error_message2=error)
    
    elif password1 == '':
        error = '入力されていません'
        return render_template('registration/signup.html', error_message3=error)
    
    elif password1 != password2:
        error = '2つのパスワードの値が異なっています'
        return render_template('registration/signup.html', error_message4=error)
    
    elif re.match(pattern, email) is None:
        error = '正しいメールアドレスの形式ではありません'
        return render_template('registration/signup.html', error_message5=error)
    
    # 重複チェック：既に登録済みのメールアドレスがあるか確認
    if PostModel.getUser(email):
        error = 'このメールアドレスは既に登録されています'
        return render_template('registration/signup.html', error_message6=error)
    


     #名前の重複チェック
    if PostModel.getUserByName(name):
        error = '既に使われています'
        return render_template('registration/signup.html', error_message7=error)

    # パスワードのハッシュ化
    password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
    
    # 入力データが検証を通過した場合、データベースに挿入
    user_id = PostModel.insert_user(name, email, password)
    if user_id:
        session['id'] = user_id  # ここで整数のユーザーIDをそのまま格納
        flash('ユーザー登録が完了しました！')
        return redirect('/login')
   
    # データベース登録が失敗した場合、何も表示せずリダイレクト
    return redirect('/signup')

# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')

    # 入力チェック
    if not email or not password:
        error = '空のフォームがあるようです'
        return render_template('registration/login.html', error_message9=error)

    # ユーザーの取得と存在チェック
    user = PostModel.getUser(email)
    if user is None:
        error = 'この会員は存在しません'
        return render_template('registration/login.html', error_message10=error)

    # パスワードのハッシュ化と照合
    hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if hashPassword != user["password"]:
        error = 'パスワードが間違っています！'
        return render_template('registration/login.html', error_message11=error)

    # ログイン成功時の処理
    session['user_id'] = user["id"]
    flash('')
    return redirect(url_for('index'))

#ホーム画面の表示
@app.route('/index')
def index():
    channels = PostModel.getChannel()
    pagetitle = "ホーム"
    return render_template('index.html', channels=channels, pagetitle=pagetitle)

#サインアウト処理
@app.route('/signout')
def signout():
    session.clear()
    return redirect('/login')

# 削除画面に遷移
@app.route('/channel_delete/<int:channel_id>')
def channel(channel_id):
    # データベースから該当のチャンネルを取得
    channel = PostModel.getChannelId(channel_id)
    if channel:
        pagetitle = "削除"
        return render_template('edit-channel/delete-channel.html',channel=channel, pagetitle=pagetitle)
    else:
        return "チャンネルが見つかりませんでした。", 404

# 部屋追加画面
@app.route('/channel_add')
def channelAddIndex():
    pagetitle = "作成"
    return render_template('edit-channel/add-channel.html', pagetitle=pagetitle)

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

# メッセージ画面
@app.route('/message/<int:channel_id>')
def messageIndex(channel_id):
    user_id = session.get("user_id")
    # データベースから該当のチャンネルを取得
    channel = PostModel.getChannelId(channel_id)
    name = PostModel.getChannelId(channel_id)
    description = PostModel.getChannelId(channel_id)
    messages = PostModel.getMessage(channel_id)
    channel_name = channel.get('name') + '部屋'
    return render_template('detail.html', channel=channel, messages=messages, user_id=user_id, name=name, description=description, pagetitle=channel_name)

# メッセージの投稿
@app.route('/message_add',methods=['POST'])
def messageAdd():
    user_id = session.get("user_id")
    content = request.form.get('content')
    channel_id = request.form.get('channel_id')
    japan_timezone = pytz.timezone('Asia/Tokyo')
    utc_now = datetime.now(timezone.utc)
    japan_time = utc_now.astimezone(japan_timezone)
    created_at = japan_time
    if content:
        PostModel.createMessage(user_id, channel_id, content, created_at)
    return redirect('/message/{channel_id}'.format(channel_id = channel_id))

    # 404エラーハンドラー
@app.errorhandler(404)
def show_error404(error):
    return render_template('error/404.html'), 404

# 500エラーハンドラー
@app.errorhandler(500)
def show_error500(error):
    return render_template('error/500.html'), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    