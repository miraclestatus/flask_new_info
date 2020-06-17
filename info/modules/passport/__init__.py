# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 19:31
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint
# 创建蓝图，并设置蓝图前缀
passport_blu = Blueprint("passport", __name__, url_prefix='/passport')

from . import views