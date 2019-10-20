# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import time
import datetime
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'zhengzhou'
url = 'http://218.28.223.13/zzzfdc/zhengzhou/permission.jsp?pn=&cn=&it=&pager.offset=0&page=1'


class Producer(TongyongSpider):
    url = 'http://218.28.223.13/zzzfdc/zhengzhou/permission.jsp?pn=&cn=&it=&page={}'

    def get_links(self, url):
        for i in range(1,5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    href = tr.xpath('./td[2]/a/@href')[0]
                    link = 'http://218.28.223.13' + href
                    print(link)
                    self.db.sadd(self.redis_db, link)
            except Exception as e:
                print(url, e)

    def run(self):
        urls = [self.url.format(i) for i in range(1, 178)]
        for url in urls:
            self.get_links(url)
            time.sleep(1)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1,5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                if response.status_code == 200:
                    text = response.text
                    html = etree.HTML(text)
                    table = html.xpath('//table[@bgcolor="#66CC33"]')[0]
                    ca_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[2]//text()')))
                    ca_time = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[4]//text()')))
                    ca_time = re.sub(r'-', '/', ca_time)
                    company = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[2]//text()')))
                    pro_name = re.sub(r'\s', '', ''.join(table.xpath('.//tr[3]/td[2]//text()')))
                    sale_info = re.sub(r'\s', '', ''.join(table.xpath('.//tr[6]/td[2]//text()')))
                    sale_num = re.search(r'(\d+)套', sale_info)
                    sale_num = sale_num.group(1) if sale_num else ''
                    area = re.sub(r'\s', '', ''.join(table.xpath('.//tr[9]/td[1]//text()')))
                    position = re.sub(r'\s', '', ''.join(table.xpath('.//tr[9]/td[2]//text()')))
                    pan_time = ''
                    price = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                    return 1
            except Exception as e:
                print(url, e)
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
                time.sleep(2)
                pass
            else:
                self.db.sadd(self.redis_db, link)

def run():
    p = Producer('HnZhengzhou:detail')
    p.run()
    c = Consumer('HnZhengzhou:detail')
    c.run()

if __name__ == '__main__':
    run()
