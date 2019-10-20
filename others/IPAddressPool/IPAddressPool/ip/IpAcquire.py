from config.SourceUrl import getUrl
from ip.Ip2Db import insert
import threading
import traceback
import requests
import logging
from logging.handlers import RotatingFileHandler
#str_fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
filehandler = logging.handlers.TimedRotatingFileHandler(
    filename="./ip池.log", when='D', interval=1, backupCount=5, encoding='utf-8'
)
logger.addHandler(filehandler)
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


def acquireIp():
    #ip地址
    aUrl = getUrl()
    logging.info('获取ip地址:{}'.format(aUrl))
    try:
        reponse = requests.get(aUrl, headers=header, timeout=5)
        if reponse.status_code == 200:
            parseHtml(reponse.text)
    except:
        # traceback.print_exc()
        logging.info('请求ip异常:{}'.format(aUrl))

#根据不同的api返回的ip格式不同，需要解析一下
def parseHtml(html):

    html = html.replace('\'', '').replace('b', '').replace('<r/>', '').replace('\r', '')
    ips = html.split("\n")
    for ip in ips:
        ip = ip.strip()
        if 'false' in ip:
            logging.info('您的套餐今日已到达上限')
            return
        elif '' == ip:
            return
        else:
            if '.' in ip:
                threading.Thread(target=insert, args=(ip,)).start()
