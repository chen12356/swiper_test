import os

from celery_task import celery_app
from libs.qn_cloud import upload_to_qiniu
from user.logics import save_avatar
from user.models import User


@celery_app.task
def upload_avatar(uid, avatar_file):
    filename, filepath = save_avatar(uid, avatar_file)  # 文件保存到本地
    avatar_url = upload_to_qiniu(filename, filepath)  # 文件上传到七牛
    User.objects.filter(id=uid).update(avatar=avatar_url)  # 保存 URL
    os.remove(filepath)  # 删除本地临时文件

@celery_app.task
def test(x,y):
    return x+y

#终端执行1：celery worker -A celery_task --loglevel=info  #启动worker

#终端执行2：celery beat -A celery_task --loglevel=INFO  #启动定期，时间到了，放到worker中执行
