import os
import re
from flask import Flask, render_template, request, redirect, make_response, flash, session
from model import PostModel  # model.pyをインポート
import hashlib

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
        flash('空の入力フォームがあります')
        return redirect('/signup')
    elif password1 != password2:
        flash('パスワードが一致しません。もう一度入力してください。')
        return redirect('/signup')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
        return redirect('/signup')
    # 重複チェック：既に登録済みのメールアドレスがあるか確認
    if PostModel.getUser(email):
        flash('このメールアドレスは既に登録されています。別のメールアドレスを使用してください。')
        return redirect('/signup')
    
    # パスワードのハッシュ化
    password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
    # IDを生成 (例: タイムスタンプとユーザー情報を使ったMD5ハッシュ)
    id = hashlib.md5(f"{name}{email}{os.urandom(16)}".encode('utf-8')).hexdigest()

    # 入力データが検証を通過した場合、データベースに挿入
    if PostModel.insert_user(name, email, password):
        UserId = str(id)
        session['id'] = UserId                     
        return redirect('/')
    else:
        flash('ユーザー登録に失敗しました。')
        return redirect('/signup')
    
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
