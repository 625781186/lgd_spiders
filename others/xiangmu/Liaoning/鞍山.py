# -*- coding: utf-8 -*-
import requests
from lxml import etree
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import re
import time
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'anshan'


# cookie有过期时间，爬之前访问一下，带cookie过去
class Producer(TongyongSpider):
    def __init__(self, redis_db):
        super(Producer, self).__init__(redis_db)
        self.url = 'http://www.zfbzfwzx.cn/Admin/KfsAdmin/ShowItemListMore.aspx?urlsort=jyzx'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Cookie': 'ASP.NET_SessionId=rncwz1g3mkuq4fogytoze10a',
        }

    def get_links(self):
        for i in range(1,5):
            try:
                response = requests.get(self.url, headers=self.headers)
                text = response.text
                html = etree.HTML(text)
                a_list = html.xpath('//a')
                for a in a_list:
                    link = 'http://www.zfbzfwzx.cn' + a.xpath('./@href')[0]
                    print(link)
                    self.db.sadd(self.redis_db, link)
            except Exception as e:
                print(e)


class Consumer(TongyongSpider):
    def __init__(self, redis_db):
        super(Consumer, self).__init__(redis_db)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Cookie': 'ASP.NET_SessionId=rncwz1g3mkuq4fogytoze10a',
        }

    def parse_detail(self, url):
        for i in range(1,5):
            try:
                response = requests.get(url, headers=self.headers)
                text = response.content.decode('gbk')
                html = etree.HTML(text)
                pro_name = ''.join(html.xpath('//span[@id="Label7"]//text()'))
                ca_num = ''.join(html.xpath('//span[@id="Label12"]//text()'))
                company = ''.join(html.xpath('//span[@id="Label3"]//text()'))
                a_list = html.xpath('//table[@id="DataList1"]//a')
                position = []
                for a in a_list:
                    build_num = ''.join(a.xpath('.//text()'))
                    position.append(build_num)
                position = ','.join(position)
                pan_time = ''
                price = ''
                ca_time = ''
                sale_num = ''
                area = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception as e:
                print(url,e)
                if i==4:
                    return 1

    def run(self):
        while True:
            set_num = self.db.scard(self.redis_db)
            if set_num == 0:
                print('数目为0')
                time.sleep(10)
                set_num2 = self.db.scard(self.redis_db)
                if set_num2 == 0: return
            link = self.db.spop(self.redis_db)
            num = self.parse_detail(link)
            if num == 1:
                time.sleep(0.1)
                pass
            else:
                self.db.sadd(self.redis_db, link)
def run():
    p = Producer('LnAnshan:Detail')
    p.get_links()
    c = Consumer('LnAnshan:Detail')
    c.run()


if __name__ == '__main__':
    run()
