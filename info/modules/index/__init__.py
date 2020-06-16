# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 18:22
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : __init__.py.py
# @Software: PyCharm

# 创建蓝图
from flask import Blueprint
index_blu = Blueprint('index', __name__)
from . import views