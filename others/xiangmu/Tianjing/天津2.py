# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime
import redis
from conf.settings import REDIS_PORT, REDIS_HOST
from threading import Thread
from common.get_ip import get_proxy

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'tianjing'

db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
redis_index2019 = 'Tianjing:index_2019'
redis_index2018 = 'Tianjing:index_2018'
redis_index2017 = 'Tianjing:index_2017'


def set_index():
    url = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2019n/index_{}.html'
    url2 = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018/index_{}.html'
    url3 = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018_3441/index_{}.html'
    urls1 = [url.format(i) for i in range(1, 38)] + ['http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2019n/index.html']
    db.sadd(redis_index2019, *urls1)
    urls2 = [url2.format(i) for i in range(1, 107)] + ['http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018/index.html']
    db.sadd(redis_index2018, *urls2)
    urls3 = [url3.format(i) for i in range(1, 663)] + ['http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018_3441/']
    db.sadd(redis_index2017, *urls3)


class Producer(TongyongSpider):
    def get_links(self, url):
        for i in range(1, 10):
            try:
                proxy = get_proxy()
                response = requests.get(url, headers=self.headers, proxies=proxy, timeout=30)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                table = html.xpath('//table[@class="table04"]')[0]
                trs = table.xpath('.//tr')[1:]
                hrefs = []
                for tr in trs:
                    href = tr.xpath('./td[2]/a/@href')[0]
                    hrefs.append(href[1:])
                return hrefs
            except Exception as e:
                print(e)

    def run(self):
        while True:
            num = self.db.scard(redis_index2019)
            if num > 0:
                url = self.db.spop(redis_index2019)
                hrefs = self.get_links(url)
                if hrefs != None:
                    for href in hrefs:
                        link = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2019n' + href
                        print(link)
                        self.db.sadd(self.redis_db, link)
            num2 = self.db.scard(redis_index2018)
            if num2 > 0:
                url = self.db.spop(redis_index2018)
                hrefs = self.get_links(url)
                if hrefs != None:
                    for href in hrefs:
                        link = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018' + href
                        print(link)
                        self.db.sadd(self.redis_db, link)
            num3 = self.db.scard(redis_index2017)
            if num3 > 0:
                url = self.db.spop(redis_index2017)
                hrefs = self.get_links(url)
                if hrefs != None:
                    for href in hrefs:
                        link = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018_3441' + href
                        print(link)
                        self.db.sadd(self.redis_db, link)
            num4 = self.db.scard(redis_index2019)
            num5 = self.db.scard(redis_index2018)
            num6 = self.db.scard(redis_index2017)
            if num4 == 0 and num5 == 0 and num6 == 0:
                return


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                proxy = get_proxy()
                response = requests.get(url, headers=self.headers, proxies=proxy,timeout=30)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                ca_time = html.xpath('//div[@class="con_Info"]/span[3]/text()')[0][3:]
                ca_time = re.sub(r'-', '/', ca_time)
                table = html.xpath('//table[@class="spfxsxk"]')[0]
                pro_name = table.xpath('.//tr[1]/td[2]/text()')[0]
                ca_num = ''.join(table.xpath('.//tr[2]/td[2]//text()'))
                ca_num = re.sub(r'\s', '', ca_num)
                company = re.sub(r'\s', '', ''.join(table.xpath('.//tr[3]/td[2]//text()')))
                area = table.xpath('.//tr[6]/td[2]/text()')[0]
                pan_time = ''
                price = ''
                sale_num = ''
                position = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception as e:
                print(url, e)
                if i == 4:
                    return 1

    def run(self):
        while True:
            set_num = self.db.scard(self.redis_db)
            if set_num == 0:
                return
            link = self.db.spop(self.redis_db)
            self.parse_detail(link)


def run():
    set_index()
    p_lis = []
    for i in range(1, 30):
        p = Producer('Tianjing:Detail')
        t = Thread(target=p.run)
        t.start()
        p_lis.append(t)
    for p in p_lis:
        p.join()
    for i in range(1, 30):
        c = Consumer('Tianjing:Detail')
        c = Thread(target=c.run)
        c.start()


if __name__ == '__main__':
    run()


    # c = Consumer('Tianjing:Detail')
    # c.parse_detail('http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018_3441/201902/t20190220_69572.html')