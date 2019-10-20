# -*- coding: utf-8 -*-
import requests
import re
import time
from lxml import etree
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime
from common.get_ip import get_proxy
import redis
from conf.settings import REDIS_PORT
from conf.settings import REDIS_HOST
from threading import Thread

city = 'jiangmen'
now = datetime.datetime.now().strftime('%Y/%m/%d')
db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

index_db = 'GdJiangmen:Detail_index'


def set_redis():
    url_jm = 'http://www.jmrea.com/ysgs_more.asp?city=%BD%AD%C3%C5&page={}'
    url_xh = 'http://www.jmrea.com/ysgs_more.asp?city=%D0%C2%BB%E1&page={}'
    url_ts = 'http://www.jmrea.com/ysgs_more.asp?city=%CC%A8%C9%BD&page={}'
    url_kp = 'http://www.jmrea.com/ysgs_more.asp?city=%BF%AA%C6%BD&page={}'
    url_ep = 'http://www.jmrea.com/ysgs_more.asp?city=%B6%F7%C6%BD&page={}'
    url_hs = 'http://www.jmrea.com/ysgs_more.asp?city=%BA%D7%C9%BD&page={}'
    urls = [url_jm.format(i) for i in range(1, 75)] + [url_xh.format(i) for i in range(1, 75)] + [
        url_ts.format(i) for i in range(1, 53)] + [url_kp.format(i) for i in range(1, 53)] + [
               url_ep.format(i) for i in range(1, 16)] + [url_hs.format(i) for i in range(1, 44)]
    db.sadd(index_db, *urls)


class Producer(TongyongSpider):
    def get_links(self, url):
        for i in range(1, 10):
            try:
                proxy = get_proxy()
                response = requests.get(url, headers=self.headers, proxies=proxy, timeout=40)
                text = response.text
                if 'The server returned an invalid or incomplete response' in text:
                    print(text)
                    continue
                html = etree.HTML(text)
                a_list = html.xpath('//a[@class="news2title"]')
                for a in a_list:
                    href = a.xpath('./@href')[0]
                    link = 'http://www.jmrea.com/' + href
                    print(link, url)
                    self.db.sadd(self.redis_db, link)
                return 1
            except Exception as e:
                print(url, e)
                if i == 9:
                    return 1

    def run(self):
        while True:
            set_num = self.db.scard(index_db)
            if set_num == 0:
                print('数目为0')
                time.sleep(10)
                set_num2 = self.db.scard(index_db)
                if set_num2 == 0: return
            href = self.db.spop(index_db)
            self.get_links(href)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 10):
            try:
                proxy = get_proxy()
                response = requests.get(url, headers=self.headers, proxies=proxy, timeout=40)
                text = response.content.decode('gbk')
                if 'The server returned an invalid or incomplete response' in text:
                    print(text)
                    continue
                pro_info = re.search(r'(批准.*?项目)', text)
                pro_info = pro_info.group(1) if pro_info else ''
                pro_info = re.sub('<.*?>', '', pro_info)
                pro_name = re.sub('(批准|项目)', '', pro_info)
                pro_name = re.sub(r'&nbsp;', '', pro_name)
                ca_num = re.search(r'编号(.*?号)', text, re.S)
                ca_num = ca_num.group(1) if ca_num else ''
                ca_num = re.sub(r'<.*?>', '', ca_num)
                ca_time = re.search(r'(\d+年.*?日)', text, re.S)
                ca_time = ca_time.group(1) if ca_time else ''
                ca_time = re.sub(r'<.*?>', '', ca_time)
                ca_time = re.sub(r'[年月]', '/', ca_time)
                ca_time = re.sub(r'日', '', ca_time)
                company = re.search(r'由<.*>(.*?公司)<.*>负责开发', text, re.S)
                company = company.group(1) if company else ''
                pan_time = ''
                price = ''
                area = ''
                sale_num = ''
                position = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception as e:
                print(url, e)
                if i == 9:
                    return 1

    def run(self):
        while True:
            set_num = self.db.scard(self.redis_db)
            if set_num == 0:
                print('数目为0')
                time.sleep(10)
                set_num2 = self.db.scard(self.redis_db)
                if set_num2 == 0: return
            href = self.db.spop(self.redis_db)
            self.parse_detail(href)


def run():
    set_redis()
    p_lis = []
    for i in range(10):
        p = Producer('GdJiangmen:Detail')
        pro = Thread(target=p.run)
        pro.start()
        p_lis.append(pro)
    for p in p_lis:
        p.join()
    for j in range(10):
        c = Consumer('GdJiangmen:Detail')
        pro = Thread(target=c.run)
        pro.start()


if __name__ == '__main__':
    run()
