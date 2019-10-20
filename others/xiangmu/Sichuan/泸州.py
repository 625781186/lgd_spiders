# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import time
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'luzhou'


class Producer(TongyongSpider):
    url = 'http://118.122.48.112:55/bit-xxzs/xmlpzs/webissue.asp?page={}'

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('gbk')
                html = etree.HTML(text)
                table = html.xpath(
                    '//table[@style="BORDER-RIGHT: #9CC7FA 0px solid; BORDER-TOP: #9CC7FA 0px solid; BORDER-LEFT: #9CC7FA 0px solid; BORDER-BOTTOM: #9CC7FA 0px solid"]')[
                    0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    href = tr.xpath('./td[2]/a/@href')[0]
                    link = 'http://118.122.48.112:55/bit-xxzs/xmlpzs/' + href
                    print(link)
                    self.db.sadd(self.redis_db, link)
                return
            except Exception as e:
                print(url, e)

    def run(self):
        for i in range(1, 28):
            self.get_links(self.url.format(i))
            time.sleep(1)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('gbk')
                html = etree.HTML(text)
                table = html.xpath(
                    '//table[@style="BORDER-RIGHT: #9CC7FA 0px solid; BORDER-TOP: #9CC7FA 0px solid; BORDER-LEFT: #9CC7FA 0px solid; BORDER-BOTTOM: #9CC7FA 0px solid"]')[
                    0]
                company = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[2]//text()')))
                company = re.sub(r'起始日期：?:?', '', company)
                pro_name = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[2]//text()')))
                ca_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[8]/td[2]//text()')))
                ca_time = table.xpath('.//tr[4]/td[2]/text()')[0]
                ca_time = re.search(r'(\d+-\d+-\d+)', ca_time).group(1)
                ca_time = re.sub(r'-', '/', ca_time)
                area = table.xpath('.//tr[3]/td[2]/text()')[0]
                table2 = html.xpath(
                    '//table[@style="BORDER-RIGHT: #9CC7FA 0px solid; BORDER-TOP: #9CC7FA 0px solid; BORDER-LEFT: #9CC7FA 0px solid; BORDER-BOTTOM: #9CC7FA 0px solid"]')[
                    1]
                trs = table2.xpath('.//tr')[1:]
                sale_num = 0
                position = []
                if len(trs) > 0:
                    for tr in trs:
                        locate = re.sub(r'\s', '', ''.join(tr.xpath('./td[2]//text()')))
                        position.append(locate)
                        num = re.sub(r'\s', '', ''.join(tr.xpath('./td[3]//text()')))
                        sale_num += int(num)
                    sale_num = str(sale_num)
                    position = ','.join(position)
                    pan_time = ''
                    price = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                else:
                    sale_num = ''
                    position = ','.join(position)
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
                time.sleep(10)
                set_num2 = self.db.scard(self.redis_db)
                if set_num2 == 0: return
            link = self.db.spop(self.redis_db)
            num = self.parse_detail(link)
            if num == 1:
                time.sleep(3)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    p = Producer('ScLuzhou:Detail')
    p.run()
    c = Consumer('ScLuzhou:Detail')
    c.run()


if __name__ == '__main__':
    run()
