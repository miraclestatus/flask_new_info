# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 17:42
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : views.py
# @Software: PyCharm
from flask import request, jsonify, current_app
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_blu
@passport_blu.route('/image_code')
def get_image_code():
    """
    1.获取参数
    :return:
    """
    ## args获取？之后的参数
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')

    if not cur_id:
        return jsonify(errno = RET.PARAMERR, errmsg='参数不全')
    try:
        name, text, image_data = captcha.generate_captcha()
        # 保存到redis里
        
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR, errmsg='验证操作失败')





