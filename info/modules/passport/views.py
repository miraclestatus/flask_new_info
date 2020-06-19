import random
from datetime import datetime

from flask import make_response, request, jsonify, current_app, json, session

from info import redis_store, constants, db
from info.libs.yuntongxun.sms import CCP
from info.models import User
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_blu
import re



#功能描述: 发送短信
# 请求路径: /passport/sms_code
# 请求方式: POST
# 请求参数: mobile, image_code,image_code_id
# 返回值: errno, errmsg
@passport_blu.route('/sms_code',methods=['POST'])
def get_sms_code():
    """
    思路分析:
    1.获取参数
    2.校验参数,为空检验,格式校验
    3.取出redis中的图片验证码
    4.判断是否过期
    5.删除redis中图片验证码
    6.正确性判断
    7.生成短信验证码
    8.发送短信
    9.判断是否发送成功
    10.保存短信验证码到redis
    11.返回响应
    """
    # 1.获取参数
    json_data = request.data
    dict_data = json.loads(json_data)
    mobile = dict_data.get('mobile')
    image_code = dict_data.get('image_code')
    image_code_id = dict_data.get('image_code_id')

    # 2.校验参数,为空检验,格式校验
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不全")

    if not re.match('1[35789]\d{9}',mobile):
        return jsonify(errno=RET.DATAERR,errmsg="手机号格式不正确")

    # 3.取出redis中的图片验证码
    try:
        redis_image_code = redis_store.get('image_code:%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据获取失败")

    # 4.判断是否过期
    if not redis_image_code:
        return jsonify(errno=RET.NODATA,errmsg="图片验证码过期")

    # 5.删除redis中图片验证码
    try:
        redis_store.delete('image_code:%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="获取失败")

    # 6.正确性判断
    if image_code.upper() != redis_image_code.upper():
        return jsonify(errno=RET.DATAERR,errmsg="图片验证码错误")

    # # 7.生成短信验证码
    sms_code = '%06d'%random.randint(0,999999)
    current_app.logger.debug('短信验证码 = %s'%sms_code )
    # 8.发送短信
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES/60],1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR,errmsg="云通讯发送失败")

    # 9.判断是否发送成功
    if result == -1:
        return jsonify(errno=RET.DATAERR,errmsg="发送短信失败")

    # 10.保存短信验证码到redis
    try:
        redis_store.set('sms_code:%s'%mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="短信保存失败")

    # 11.返回响应
    return jsonify(errno=RET.OK,errmsg="发送成功")


#功能描述: 图片验证码
#请求地址: /passport/image_code
#请求方式: GET
#请求参数: 随机字符串(uuid)cur_id, 上一个字符串:pre_id
#返回值:  返回图片
@passport_blu.route('/image_code')
def get_image_code():

    """
    思路分析:
    1.获取参数
    2.校验参数
    3.生成图片验证码
    4.保存到redis
    5.返回
    :return:
    """

    #1.获取参数
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')

    #2.校验参数
    if not cur_id:
        return jsonify(errno=RET.PARAMERR,errmsg='参数不全')

    #3.生成图片验证码
    try:
        name,text,image_data = captcha.generate_captcha()

        #4.保存到redis
        #参数1:保存到redis的key
        #参数2:图片验证码
        #参数3:过期时间
        redis_store.set('image_code:%s'%cur_id,text,constants.IMAGE_CODE_REDIS_EXPIRES)

        #判断有没有上个编号
        if pre_id:
            redis_store.delete('image_code:%s'%pre_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="验证操作失败")

    #5.返回图片验证码
    response = make_response(image_data)
    response.headers["Content-Type"] = 'image/jpg'
    return response
