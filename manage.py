# -*- coding: utf-8 -*-
# @Time    : 2020/6/15 17:43
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : manage.py 只负责基本的启动工作，
# app 的创建在 info 下的__init__ 中
# @Software: PyCharm
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import app, db
# flask_script
manager = Manager(app)
# 数据库迁移
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    session['name'] = 'eric'
    return "index"
if __name__ == '__main__':
    manager.run()