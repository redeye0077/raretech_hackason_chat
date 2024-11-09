import os
import re
from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from model import PostModel  # model.pyをインポート

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
    else:
        # 入力データが検証を通過した場合、データベースに挿入
        PostModel.insert_user(name, email, password1)
        # Cookieに保存
        resp = make_response(redirect('/'))
        resp.set_cookie('last_post', email)
        return resp

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
