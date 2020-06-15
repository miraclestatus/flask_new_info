# -*- coding: utf-8 -*-
# @Time    : 2020/6/15 17:43
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : manage.py.py
# @Software: PyCharm
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

app = Flask(__name__)

class Config(object):
    """工程信息配置"""
    DEBUG = True
    # 导入数据库配置
    # 设置数据库连接
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/information22'
    # 动态追踪设置
    app.config['SQLALCHEMY_TRACK_MODUFICATIONS'] = True
    # 显示原始sql
    app.config['SQLALCHEMY_ECHO'] = True

    RDIES_HOST = "127.0.0.1"
    RDIES_PORT = 6379
@app.route('/')
def index():
    return "index"
if __name__ == '__main__':
    app.run()