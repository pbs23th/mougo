from flask import Blueprint ,render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import pymysql
from . import sqlsetting



auth = Blueprint('auth', __name__)

@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        print(email)
        password = request.form.get('password')
        print(password)

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('로그인 성공', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('비밀번호가 틀렸습니다.', category='error')
        else:
            flash('아이디가 없습니다', category='error')



    return render_template('login.html', user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign_up", methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        if not(email and username and password and re_password):
            flash('입력하지않는 값이 있습니다.', category='error')
        elif password != re_password:
            flash('비밀번호가 틀렸습니다.', category='error')
        else:
            new_User = User(email = email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_User)
            db.session.commit()
            flash('회원가입 성공.', category='success')
            return redirect(url_for("views.home"))
    return render_template('sign_up.html', user=current_user)
