'''
1.包含应用工厂create_app()
2.flaskr为一个包
'''
import os
from flask.views import View
from flask import Flask

'''
flask会自动从环境变量FLASK_APP的值定义的模块中寻找
名称为create_app()或make_app()的工厂函数，自动调用
工厂函数创建程序实例并运行。因为我们已经在.flaskenv
文件中将FLASK_APP设为personalBlog，所以不需要更改
任何设置，继续使用flask run命令即可运行程序：
'''
def create_app(test_config=None):
    # 创建并配置app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite')
    )
    if test_config is None:
        # 实例配置
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 测试配置
        app.config.from_mapping(test_config)

    # 如果没有instance文件夹，则创建
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 
    @app.route('/hello')
    def hello():
        return 'Hello, w'

    # 注册数据库
    from . import db
    db.init_app(app)

    # 注册蓝图
    from . import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    app.add_url_rule('/', endpoint='index')
    
    return app
