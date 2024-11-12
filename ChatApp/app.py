import os
import re
from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session
from model import PostModel  # model.pyをインポート
from ast import Return
import hashlib
from util.DB import DB

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

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
        error = '空の入力フォームがあります'
        return render_template('registration/signup.html', error_message1=error)
    
    elif password1 != password2:
        error = 'パスワードが一致しません。もう一度入力してください。'
        return render_template('registration/signup.html', error_message2=error)
    
    elif re.match(pattern, email) is None:
        error = '正しいメールアドレスの形式ではありません'
        return render_template('registration/signup.html', error_message3=error)
    
    # 重複チェック：既に登録済みのメールアドレスがあるか確認
    if PostModel.getUser(email):
        error = 'このメールアドレスは既に登録されています。別のメールアドレスを使用してください。'
        return render_template('registration/signup.html', error_message4=error)

     #名前の重複チェック
    if PostModel.getUserByName(name):
        error = 'この名前は既に使用されています。別の名前を使用してください。'
        return render_template('registration/signup.html', error_message5=error)

    # パスワードのハッシュ化
    password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
    
    # 入力データが検証を通過した場合、データベースに挿入
    if PostModel.insert_user(name, email, password):
        session['id'] = str(id)
        flash('ユーザー登録が完了しました！')
        return redirect('/login')
   
    else:
        error = 'ユーザー登録に失敗しました。'
        return render_template('registration/signup.html', error_message6=error)

# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
