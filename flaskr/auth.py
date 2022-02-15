import functools

from flask import (
    Blueprint, flash, g, redirect,  render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# 创建蓝图，类似创建app
bp = Blueprint('auth', __name__, url_prefix='/auth')

# 注册
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = "请输入用户名"
        elif not password:
            error = "请输入密码"
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"用户名{username}已被占用"
            else:
                return redirect(url_for("auth.login"))
                
        flash(error)

    return render_template('auth/register.html')

# 登录
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = '查无此人'
        elif not check_password_hash(user['password'], password):
            error = '密码错误'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# 更新g.user，在视图函数前运行
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# 注销
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# 装饰器,用来检测用户是否登录
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None: # 未登录，跳转到登录页面
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

