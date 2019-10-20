# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import time
from common.spider_class import TongyongSpider
from common.update_mongo import Update
from common.update_mongo import Update2
import datetime
import os

path=os.path.dirname(__file__)
file='city.txt'

city = 'longyan'
now = datetime.datetime.now().strftime('%Y/%m/%d')


class Producer(TongyongSpider):
    url = 'http://222.78.94.14/ZL/House/Link/YSXXCX?pagenumber={}&pagesize=15'

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                trs = html.xpath('//table//tr')[1:]
                for tr in trs:
                    ca_time = ''.join(tr.xpath('./td[6]//text()'))
                    href = tr.xpath('./td[7]/a/@href')[0]
                    company = ''.join(tr.xpath('./td[3]//text()'))
                    link = 'http://222.78.94.14' + href
                    print(link)
                    self.db.sadd('FjLongyan:Detail', link + '<<<' + ca_time + '<<<' + company)
                return
            except Exception as e:
                print(url, e)
                if i == 4: return

    def run(self):
        for i in range(1, 48):
            self.get_links(self.url.format(i))
            time.sleep(1)


class Consumer(TongyongSpider):
    def parse_detail(self, url, ca_time, company):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table[@class="table tablestyles"]')[0]
                pro_name = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[2]//text()')))
                position = re.search(r'“.*”(.*?)', pro_name)
                position = position.group(1) if position else ''
                ca_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[1]//text()')))
                ca_time = ca_time
                sale_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[13]/td[2]//text()')))
                area = re.sub(r'\s', '', ''.join(table.xpath('.//tr[13]/td[3]//text()')))
                ca_time = re.sub(r'-', '/', ca_time)
                pan_time = ''
                price = ''
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
                print('数目为0')
                time.sleep(100)
                set_num2 = self.db.scard(self.redis_db)
                if set_num2 == 0: return
            link = self.db.spop(self.redis_db)
            url = link.split('<<<')[0]
            ca_time = link.split('<<<')[1]
            company = link.split('<<<')[2]
            num = self.parse_detail(url, ca_time, company)
            if num == 1:
                time.sleep(2)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    try:
        p = Producer('FjLongyan:Detail')
        p.run()
        c = Consumer('FjLongyan:Detail')
        c.run()
    except Exception as e:
        file_path=os.path.join(path,file)
        with open(file_path,'at',encoding='utf-8') as fp:
            fp.write(str(e))
            fp.write('\r')


if __name__ == '__main__':
    run()
