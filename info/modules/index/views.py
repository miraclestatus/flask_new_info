# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 18:22
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : views.py
# @Software: PyCharm


# 蓝图
from flask import render_template

from . import index_blu
@index_blu.route('/')
def index():
    # return "index"
    return render_template('news/index.html')