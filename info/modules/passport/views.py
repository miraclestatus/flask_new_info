# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 17:42
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : views.py
# @Software: PyCharm
import random
import re
from info.libs.yuntongxun.sms import CCP
import redis
from flask import request, jsonify, current_app, make_response, json

from info import redis_store, constants
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_blu


# 发送短信验证码
@passport_blu.route('/sms_code', methods =['POST'])
def get_sms_code():
    """

    :return:
    """
    # 获取参数
    json_data = request.data
    # json —————— 》 dict
    dict_data = json.loads(json_data)
    mobile = dict_data.get('mobile')
    image_code = dict_data.get('image_code')
    image_code_id = dict_data.get('image_code_id')

    # 校验
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不全')

    # 手机号
    if not re.match('1[35789]\d{9}', mobile):
        return jsonify(errno=RET.DATAERR, errmsg='手机号格式不对')
    # 取出redis的验证码

    try:
        # 保存到redis里
        redis_image_code = redis_store.get('image_code:%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR, errmsg='redis数据操作失败')


    # 判断验证码是否过期
    if not redis_image_code:
        return jsonify(errno=RET.NODATA, errmsg='redis验证码过期')

    # 删除redis验证码
    try:
        redis_store.delete('image_code:%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DATAERR, errmsg='数据操作失败')

    # 验证码正确性判断
    if image_code.upper() != redis_image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg='图片验证码错误')
    # 生成短信验证码
    sms_code = '%06d%'%random.randint(0,999999)
    current_app.logger.debug('短信验证码是 = {}'.format(sms_code))
    # TODO 调用云通讯
    try:
        ccp = CCP()
        # 注意： 测试的短信模板编号为1
        # 参数1: 发送给谁的手机号
        # 参数2: ['内容', 有效时间单位分钟]
        # 参数3: 模板编号1  【云通讯】您使用的是云通讯短信模板，您的验证码是{1}，请于{2}分钟内正确输入

        result = ccp.send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES/60], 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='云通讯失败')
    # 判断是否发送成功
    if result == -1:
        return jsonify(errno=RET.DATAERR, errmsg='发送失败')

    # 保存验证到redis中

    try:
        redis_store.set('sms_code:%s' % mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='短信保存失败')
    return jsonify(errno = RET.OK, errmsg='发送成功')
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
        redis_store.set('image_code:%s'%cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            redis_store.delete('image_code:%s'%pre_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR, errmsg='验证操作失败')
    # 返回验证码图片
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    return response





