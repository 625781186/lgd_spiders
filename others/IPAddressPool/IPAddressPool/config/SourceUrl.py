import random
from db.RedisUtils import RedisQueue
import logging
from logging.handlers import RotatingFileHandler

#str_fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
filehandler = logging.handlers.TimedRotatingFileHandler(
    filename="./ip池.log", when='D', interval=1, backupCount=5, encoding='utf-8'
)
logger.addHandler(filehandler)

urls = [
    ''    #放入第三方ip接口
]

def getUrl():
    u = []
    for i in urls:
        u.append(str(i, encoding='utf-8'))
    return u[random.randint(0, len(u) - 1)]  # 随机返回urls

# #连接redis数据库
# redis = RedisQueue("ip_url")
# for i in urls:
#     redis.put(i)
#
#
# def getUrl():
#     url = redis.getAll()
#     u = []
#     for i in url:
#         u.append(str(i, encoding='utf-8'))
#     return u[random.randint(0, len(u) - 1)]  # 随机返回urls


# if __name__ == '__main__':
#     logging.info(getUrl())
