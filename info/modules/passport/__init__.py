# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 17:42
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint
passport_blu = Blueprint("passport", __name__, url_prefix='/passport')
from . import views