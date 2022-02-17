from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from urllib3 import Retry
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

# 主页展示帖子
@bp.route('/')
def index():
    db = get_db()   # sql?
    posts = db.execute( 
        'SELECT p.id, title, body, created, author_id, username '
        'FROM post p JOIN user u ON p.author_id = u.id '
        'ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

# 创建新帖
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = '请填写标题'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id) '
                'VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

# 获取帖子
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username '
        'FROM post p '
        'JOIN user u ON p.author_id = u.id '
        'WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"#{id}帖子不存在")
    if check_author and post['author_id'] != g.user['id']: # 本人访问
        abort(403, "无权访问")

    return post

# 更新帖子
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = '请填写标题'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? '
                'WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

# 删除帖子
@bp.route('/<int:id>/delete', methods=('POST',)) # 必须加逗号
@login_required
def delete(id):
    get_post(id)    # 检查id是否存在
    db = get_db()
    db.execute('DELETE FORM post WHERE id = ?', (id))
    db.commit()
    return redirect(url_for('blog.index'))

def get_comment(id):
    comm = get_db().execute(
        'SELECT content FROM comment WHERE post_id = ?',
        (id,)
    ).fetchall()
    return comm

# 文章详情
@bp.route('/post/<int:id>', methods=('GET','POST'))
def show(id):
    # 评论
    if request.method == 'POST':
        comm = request.form['comm_content']
        db = get_db()
        db.execute(
            'INSERT INTO comment (post_id, content) '
            'VALUES (?, ?)',
            (id, comm)
        )
        db.commit()
    post = get_post(id,check_author=False)
    comm = get_comment(id)
    return render_template('blog/post.html',post=post,comments=comm)

def get_profile(uid):

    prof = get_db().execute(
        'SELECT id, username FROM user WHERE id = ?',
        (uid,)
    ).fetchone()
    posts = get_db().execute(
        'SELECT id, title FROM post WHERE author_id = ?',
        (uid,)
    ).fetchall()

    return prof, posts


# 个人资料
@bp.route('/profile/<int:uid>', methods=('GET',))
def profile(uid):
    prof, posts = get_profile(uid)
    return render_template('blog/profile.html',prof=prof, posts=posts)

# 点赞
# @bp.route('/<int:id>/like/<string:action>', methods=('GET',))
# def like(id,action):
#     action_string = action+'_num'
#     db = get_db()
#     num = db.execute(
#         'SELECT '+action_string+' FROM post WHERE id = ?',
#         (id,)
#     ).fetchone()
#     num[action_string]+=1
#     db.execute(
#         'UPDATE post SET '+action_string+' = '+num[action_string]+' WHERE id = ?',
#         (id,)
#     )
#     db.commit()



