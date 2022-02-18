# Flask博客模板

## 使用方法

使用Powershell

### 使用venv(可跳过)

``` powershell
.\venv\Scripts\activate
```

### 设置环境变量

``` powershell
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
```

### 初始化数据库

``` powershell
flask init-db
```

### 启动

``` py
flask run
```

## 功能

贴子，个人资料，评论

## 待改进

* 点赞
* 收藏
* 搜索框
* 分页
* 上传图片
* 蓝图重新设计
* 改进css，html分类
