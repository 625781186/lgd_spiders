import threading
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
#获取到新的ip
def insert(ip):
    logging.info("获取新的ip：{}".format(str(ip)))
    for db in pools:
        threading.Thread(target=insertOne, args=(ip, db.getInputMethod(), db, db.getDesc())).start()


def insertOne(ip, fun, db, sign):
    try:
        if fun(ip):
            db.insert_mongo(ip)
            logging.info('入库{}ip:{}'.format(sign, ip))
    except:
        pass
