# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 11:39
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : views.py
# @Software: PyCharm
from flask import render_template, current_app, session

from info import constants
from info.models import User, News
from . import index_blu
@index_blu.route('/')
def index():
    """首页显示"""
    # 获取当前登录用户的id
    user_id = session.get("user_id")
    # 通过id查询用户信息
    user = None
    news_list = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)
    click_news_list =  []
    for news in news_list if news_list else []:
        click_news_list.append(news.to_basic_dict())
    data = {
        "user_info": user.to_dict() if user else None,
        "click_news_list":click_news_list,
    }

    return render_template('news/index.html',data=data )
    # return "dada"





#浏览器在访问,在访问每个网站的时候,都会发送一个Get请求,向/favicon.ico地址获取logo
#app中提供了方法send_static_file,会自动寻找static静态文件下面的资源
@index_blu.route('/favicon.ico')
def get_web_logo():

    return current_app.send_static_file('news/favicon.ico')

