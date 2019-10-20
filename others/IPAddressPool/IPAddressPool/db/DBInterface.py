# from db.RedisDb import RedisDb
from db.MongoDb import MongoDBUtil as mongo
import logging
from logging.handlers import RotatingFileHandler
#str_fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
filehandler = logging.handlers.TimedRotatingFileHandler(
    filename="./ip池.log", when='D', interval=1, backupCount=5, encoding='utf-8'
)
logger.addHandler(filehandler)

class DBInterface:
    def __init__(self, col, input_verify, forVerify, describe):
        #先导入mongo，self.instance是一个mongo连接的对象
        self.instance = mongo(col)
        self.inDbVerifyMethod = input_verify
        self.forVerifyMethod = forVerify
        self.describe = describe
    #删除数据库mongo的内容，都是调用mongo的方法
    def delect(self):
        logging.info('删除无用ip:{}-->{}'.format(self.getDesc(), self.instance.delect()))
    #更新mongo数据库
    def updata(self, ip, isValid):
        self.instance.updata(ip, isValid)
    #获取mongo数据库内的所有信息并返回出去，
    def select_all(self):
        return self.instance.select_all()

    def select_all_available_ip(self):
        return self.instance.select_all_available_ip()

    def insert_mongo(self, ip):
        self.instance.insert_mongo(ip)
#以下两个方法一致都是调用的传入该类的第二个，第三个参数是验证ip的，返回True或者是False
    def getInputMethod(self):
        return self.inDbVerifyMethod

    def getForVerifyMethod(self):
        return self.forVerifyMethod
    #传出去自定义的标识字段
    def getDesc(self):
        return self.describe
