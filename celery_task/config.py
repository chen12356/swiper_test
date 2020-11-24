from celery.schedules import crontab

broker_url = 'redis://127.0.0.1:6379/10'
broker_pool_limit = 10  # Borker 连接池, 默认是10

timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']
task_serializer = 'pickle'

result_backend = 'redis://127.0.0.1:6379/10'
result_serializer = 'pickle'
result_cache_max = 10000  # 任务结果最大缓存数量
result_expires = 3600  # 任务结果过期时间
include = ['celery_task.tasks']

beat_schedule={
     "test_task":{
         "task":"celery_task.tasks.test",  # 需要被执行的任务(函数)
         "schedule":10, # 每10秒钟执行一次
         "args":(10,10)  #参数
     },
     "each1m_task": {
         "task": "celery_task.tasks.test",
         "schedule": crontab(minute=1), # 每一分钟执行一次
         "args": (10, 20)
     },
     "each24hours_task": {
         "task": "celery_task.tasks.test",
         "schedule": crontab(hour=23), # 每24小时执行一次
         "args": (10, 30)
     }
}

worker_redirect_stdouts_level = 'INFO'