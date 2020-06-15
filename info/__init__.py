# -*- coding: utf-8 -*-
# @Time    : 2020/6/15 19:21
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config
app = Flask(__name__)

def create_app(config):
    pass

app.config.from_object(Config)
db = SQLAlchemy(app)
# 初始化redis配置
# redis.StrictRedis(host=Config.RDIES_HOST, port=Config.RDIES_PORT)

# 开启csrf 保护， 只用于服务器验证功能
CSRFProtect(app)
# 设置session保存指定位置
Session(app)
