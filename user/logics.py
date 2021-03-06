import random
import logging

import requests
from django.core.cache import cache

from swiper import config
from common import keys

inf_log = logging.getLogger('inf')


def gen_random_code(length=6):
    '''产生指定长度的随机码'''
    # 香平解法
    # return str(random.randint(10 ** (length - 1), 10 ** length - 1))

    # 建港解法
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def send_vcode(mobile):
    '''
    发送短信验证码

    用户 -> 自己服务器 -> 短信平台 -> 发送短信
    '''
    vcode = gen_random_code()  # 产生验证码
    inf_log.debug('状态码: %s' % vcode)

    args = config.YZX_SMS_ARGS.copy()  # 浅拷贝全局配置
    args['param'] = vcode
    args['mobile'] = mobile

    # 调用第三方接口发送验证码
    response = requests.post(config.YZX_SMS_API, json=args)

    # 检查结果
    if response.status_code == 200:
        result = response.json()
        if result['msg'] == 'OK':
            cache.set(keys.VCODE_K % mobile, vcode, 180)  # 将验证码写入缓存，保存 3 分钟
            return True
    return False


def save_avatar(uid, avatar_file):
    '''将个人形象保存到本地'''
    filename = 'Avatar-%s' % uid
    filepath = '/tmp/%s' % filename
    with open(filepath, 'wb') as fp:
        for chunk in avatar_file.chunks():
            fp.write(chunk)
    return filename, filepath


