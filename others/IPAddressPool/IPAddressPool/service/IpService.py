import threading
from ip.IpAcquire import acquireIp

from my_pool.Pool_ip import pools
import logging
from logging.handlers import RotatingFileHandler
#str_fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
filehandler = logging.handlers.TimedRotatingFileHandler(
    filename="./ip池.log", when='D', interval=1, backupCount=5, encoding='utf-8'
)
logger.addHandler(filehandler)

def deleteIp():
    for db in pools:
        db.delect()


def testIp():
    #pools里面的每一个对象，将对象作为参数传给
    for db in pools:
        threading.Thread(target=testDB, args=(db,)).start()

#这个db参数就是传递过来的对象，执行这个select_all的方法
def testDB(db):
    #参数i就是无效的ip，调用testone方法
    for i in db.select_all():
        threading.Thread(target=testOne, args=(i, db.getForVerifyMethod(), db, db.getDesc())).start()


def acquire(num):
    for i in range(0, num):
        acquireIp()

#接收4个参数，第一个是ip，第二个是一个验证ip方法的执行结果，第三个是数据库Mongo的对象，第四个是自定义的标识符
def testOne(ip, fun, db, sign):
    if fun(ip):
        #把所有不能用的ip在测试一下成功就入库更新
        db.updata(ip, 1)
        logging.info('{}ip:{}有效'.format(sign, ip))
    else:
        db.updata(ip, 0)
        logging.info('{}ip:{}不可用'.format(sign, ip))
#执行效果就是该ip是否可用