import time
import threading
from service.IpService import testIp
from service.IpService import acquire
from service.IpService import deleteIp
import traceback

import logging
from logging.handlers import RotatingFileHandler
#str_fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
filehandler = logging.handlers.TimedRotatingFileHandler(
    filename="./ip池.log", when='D', interval=1, backupCount=5, encoding='utf-8'
)
logger.addHandler(filehandler)
def main():
    #开启日志
    logging.info('程序启动')
    try:
        #开启两个线程，一个获取ip,一个更新ip同时进行
        threading.Thread(target=checkIpMain).start()
        threading.Thread(target=updata).start()
    except:
        main()

#开启线程调用的更新ip的方法
def updata():
    cc = 0
    logging.info('更新线程启动！！！')
    while (True):
        try:
            #调用方法
            acquire(1)
            time.sleep(5)
            cc += 1
        except:
            traceback.print_exc()
            logging.info("更新时有异常。。。。")
            time.sleep(2)

#更新Ip线程调用的方法，把不可用的ip在进行重新测试入库
def checkIpMain():
    while True:
        try:
            logging.info('测试线程执行！！！')
            testIp()
            deleteIp()
            time.sleep(10)
        except:
            traceback.print_exc()
            logging.info("测试时有异常。。。。")
            time.sleep(2)

#程序从这里启动，先调用main方法
if __name__ == '__main__':
    main()
