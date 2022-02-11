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
            print('----',email)
            insert_user_data(email)
            flash('회원가입 성공.', category='success')
            return redirect(url_for("views.home"))
    return render_template('sign_up.html', user=current_user)

def insert_user_data(email):
    connection = sqlsetting.mysqlset()
    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''select id from trade.user where email = %s'''
    my_cursor.execute(sql, email)
    select_data = my_cursor.fetchone()
    connection.commit()

    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''insert into trade.okex_buyintervalset(buy_1,buy_2,buy_3,buy_4,buy_5,buy_6,buy_7,buy_8,buy_9, userid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    my_cursor.execute(sql, (0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3, select_data['id']))
    connection.commit()
    #
    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''insert into trade.upbit_buyintervalset(buy_1,buy_2,buy_3,buy_4,buy_5,buy_6,buy_7,buy_8,buy_9, userid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    my_cursor.execute(sql, (0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3, select_data['id']))
    connection.commit()

    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''insert into trade.bitmex_buyintervalset(buy_1,buy_2,buy_3,buy_4,buy_5,buy_6,buy_7,buy_8,buy_9, userid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    my_cursor.execute(sql, (0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3, select_data['id']))
    connection.commit()

    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''insert into trade.okex_setting(apikey,secretkey,start_payment,currency,botstatus,count,positionsell,payment, loss_stop,
     stoploss_onoff, passphrase, brokerid, stepprice, unitformat, appointment, userid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    my_cursor.execute(sql, (str(0), str(0), float(10), str('BTC'), int(0), int(5), float(0.5), str('USDT'), float(0), int(0), str(0), str('e7c64c9dec0944BC'), str(0), str(0), int(0), select_data['id']))
    connection.commit()

    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''insert into trade.upbit_setting(apikey,secretkey,start_payment,currency,botstatus,count,positionsell,payment,loss_stop,
     stoploss_onoff, appointment, userid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    my_cursor.execute(sql, (str(0), str(0), float(10000), str('BTC'), int(0), int(5), float(0.5), str('KRW'), float(0), int(0), int(0), select_data['id']))
    connection.commit()

    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''insert into trade.bitmex_setting(apikey,secretkey,start_payment,currency,botstatus,count,positionsell,payment, entry_position, loss_stop, stoploss_onoff, appointment, userid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    my_cursor.execute(sql, (str(0), str(0), float(100), str('XBTUSD'), int(0), int(5), float(0.5), str('XBT'), str("long"), float(0), int(0), int(0), select_data['id']))
    connection.commit()





    connection.close()
    return 200
