import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, sbort, \
    render_template, flash

FLASKR_SETTINGS = ''

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# 连接数据库
def connect_db():
    # 连接数据库
    rv = sqlite3.connect(app.config['DATABASE'])
    # 使得可以通过字典而不是元组访问行(row)
    rv.row_factory = sqlite3.Row
    return rv

if __name__=='__main__':
    app.run()