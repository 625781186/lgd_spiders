# coding=utf-8
import redis
import requests
import time
import datetime
from multiprocessing import Process
import datetime

d = datetime.datetime.now().strftime('%Y-%m-%d %X')

host = '127.0.0.1'
db = redis.StrictRedis(host=host, port=6379, decode_responses=True)
ip = db.srandmember('ProxiesIP')
# print(ip)
proxy = {
    'http': '%s' % ip,
    'https': '%s' % ip
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}


# response = requests.get('https://www.landchina.com/', proxies=proxy, timeout=3, headers=headers)
# response = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=10, headers=headers)
# print(response.text)


def test():
    while True:
        try:
            ip = db.srandmember('ProxiesIP')
            proxy = {
                'http': '%s' % ip,
                'https': '%s' % ip
            }
            s = time.time()
            response = requests.get('https://www.landchina.com/', proxies=proxy, headers=headers)
            e = time.time()
            print(response.status_code, e - s)
        except Exception as e:
            print(e)
            with open(r'D:\xiangmu\rizhi.txt', 'at') as f:
                d = datetime.datetime.now().strftime('%Y-%m-%d %X')
                f.write(str(e) + '  ' + d)
                f.write('\r\n')


if __name__ == '__main__':
    with open(r'D:\xiangmu\rizhi.txt', 'wt') as f:
        f.write(d + ' ' + '开始测试')
        f.write('\r\n')
    for i in range(15):
        p = Process(target=test)
        p.start()
