import redis
import asyncio
import aiohttp
import time
import requests
import json
from threading import Thread


class Proxiesip_Pool_ADD(Thread):
    test_url = 'http://www.baidu.com'
    url = 'https://dps.kdlapi.com/api/getdps/?orderid=996275312756347&num=5&pt=1&format=json&sep=1'

    def __init__(self):
        super(Proxiesip_Pool_ADD, self).__init__()
        self.db = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)

    def add_ip(self):
        '''
        添加代理到redis
        :return:
        '''
        response = requests.get(self.url)
        text = response.text
        text = json.loads(text)
        ips = text['data']['proxy_list']
        for ip in ips:
            self.db.sadd('ProxiesIP', ip)
        print('添加ip', ips, '成功')

    def run(self):
        while True:
            self.add_ip()
            time.sleep(400)


class Proxiesip_Pool_Test(Thread):
    test_url = 'http://www.baidu.com'
    url = 'https://dps.kdlapi.com/api/getdps/?orderid=996275312756347&num=5&pt=1&format=json&sep=1'

    def __init__(self):
        super(Proxiesip_Pool_Test, self).__init__()
        self.db = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)

    async def test_single_proxy(self, proxy):
        '''
        测试单个代理
        :param proxy: 待测试的代理
        :return:
        '''
        conn = aiohttp.TCPConnector(ssl=False)
        real_proxy = 'http://' + proxy
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                async with session.get(self.test_url, proxy=real_proxy, timeout=10,
                                       allow_redirects=False) as response:
                    if response.status == 200:
                        print('代理可用', proxy)
            except Exception:
                print('删除代理', proxy)
                self.db.srem('ProxiesIP', proxy)

    def test_all(self):
        proxies = list(self.db.smembers('ProxiesIP'))
        count = len(proxies)
        for i in range(0, count, 10):
            start = i
            stop = min(i + 10, count)
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in proxies[start:stop]]
            loop.run_until_complete(asyncio.wait(tasks))
            time.sleep(10)


if __name__ == '__main__':
    p = Proxiesip_Pool_ADD()
    p.start()
