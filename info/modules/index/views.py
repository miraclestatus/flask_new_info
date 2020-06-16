# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 18:22
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : views.py
# @Software: PyCharm


# 蓝图
from flask import render_template, current_app

from . import index_blu
@index_blu.route('/')
def index():
    # return "index"
    return render_template('news/index.html')
@index_blu.route('/favicon.ico')
def get_web_logo():
    return current_app.send_static_file('news/favicon.ico')
