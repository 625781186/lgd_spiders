# -*- coding: utf-8 -*-
from common.spider_class import TongyongSpider
import requests
from lxml import etree
import re
from common.update_mongo import Update
from common.update_mongo import Update2
import time
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'kaifeng'


class Producer(TongyongSpider):
    url = 'http://www.kfjs.gov.cn/xzxkgs/{}/'

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                a_list = html.xpath('//li[@class="nwes_list_li"]//a')
                for a in a_list:
                    title = a.xpath('./@title')[0]
                    if '商品房预售' in title:
                        link = a.xpath('./@href')[0]
                        print(link)
                        self.db.sadd(self.redis_db, link)
            except Exception as e:
                print(e)

    def run(self):
        for i in range(1, 3):
            self.get_links(self.url.format(i))


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                table = html.xpath('//table')[0]
                trs = table.xpath('.//tr')[2:]
                for tr in trs:
                    pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[1]//text()')))
                    company = re.sub(r'\s', '', ''.join(tr.xpath('./td[2]//text()')))
                    ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                    position = re.sub(r'\s', '', ''.join(tr.xpath('./td[5]//text()')))
                    start_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[6]//text()')))
                    pan_time = start_time.split('-')[0]
                    pan_time = re.sub(r'\.', '/', pan_time)
                    price = ''
                    ca_time = ''
                    sale_num = ''
                    area = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                return 1
            except Exception:
                print('解析异常')
                if i == 4:
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
                # time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    p = Producer('HnKaifeng:Detail')
    p.run()
    c = Consumer('HnKaifeng:Detail')
    c.run()


if __name__ == '__main__':
    run()
