# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
from common.spider_class import TongyongSpider
import time
from common.update_mongo import Update
from common.update_mongo import Update2
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'jinzhong'


class Producer(TongyongSpider):
    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//div[@class="mBd"]/table')[0]
                trs = table.xpath('./tr')[1:]
                for tr in trs:
                    ca_time = tr.xpath('./td[5]//text()')[0]
                    href = tr.xpath('./td[3]/a/@href')[0]
                    link = 'http://www.sxjz.gov.cn' + href
                    zoom = link + '<<<' + ca_time
                    print(zoom)
                    self.db.sadd(self.redis_db, zoom)
            except Exception as e:
                print(url, e)

    def run(self):
        for i in range(1, 5):
            self.get_links('http://www.sxjz.gov.cn/publicity_zjj/spzl_{}'.format(i))


class Consumer(TongyongSpider):
    def parse_detail(self, url, ca_time):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table[@class="govDetailTable"]')[0]
                ca_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[3]/td[2]//text()')))
                content = re.sub(r'\s', '', ''.join(html.xpath('//div[@class="govIntro"]//text()')))
                company = re.search(r'(.*?公司)', content)
                company = company.group(1) if company else ''
                if not ca_num:
                    ca_num = re.search(r'(晋房.*?\d+-\d+)', content)
                    ca_num = ca_num.group(1) if ca_num else ''
                if '公司' in content:
                    pro_name = content.split('公司')[1]
                else:
                    pro_name = content
                table = html.xpath('//table')
                if len(table) > 1:
                    table = html.xpath('//table')[1]
                    trs = table.xpath('.//tr')[1:]
                    for tr in trs:
                        pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[1]//text()')))
                        ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                        pan_time = ''
                        price = ''
                        area = ''
                        sale_num = ''
                        position = ''
                        build = (
                        pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                        print(build)
                        Update2(build, city)
                else:
                    pan_time = ''
                    price = ''
                    sale_num = ''
                    area = ''
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
                print('数目为0')
                time.sleep(10)
                set_num2 = self.db.scard(self.redis_db)
                if set_num2 == 0: return
            zoom_link = self.db.spop(self.redis_db)
            link = zoom_link.split('<<<')[0]
            ca_time = zoom_link.split('<<<')[1]
            ca_time = re.sub(r'-', '/', ca_time)
            num = self.parse_detail(link, ca_time)
            if num == 1:
                # time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, zoom_link)


def run():
    p = Producer('SxJinzhong:Detail')
    p.run()
    c = Consumer('SxJinzhong:Detail')
    c.run()


if __name__ == '__main__':
    run()
