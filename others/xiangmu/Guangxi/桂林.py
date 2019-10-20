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
city = 'guiling'


# 核发日期=发布时间
class Producer(TongyongSpider):
    url = 'http://fcxx.glzjxx.com/website/notice/sell/index.html?page={}'

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                a_list = html.xpath('//div[@class="list_mian_right"]//li//a')
                time_infos = html.xpath('//span[@class="style_newslist_time"]')
                for a, time_info in zip(a_list, time_infos):
                    href = a.xpath('./@href')[0]
                    link = 'http://fcxx.glzjxx.com/website/notice/sell/' + href
                    ca_time = time_info.xpath('./text()')[0]
                    ca_time = re.search(r'(\d+-\d+-\d+)', ca_time).group(1)
                    print(link)
                    self.db.sadd(self.redis_db, link + '<<<' + ca_time)
                return
            except Exception as e:
                print(url, e)

    def run(self):
        for i in range(1, 56):
            self.get_links(self.url.format(i))
            time.sleep(2)


class Consumer(TongyongSpider):
    def parse_detail(self, url, ca_time):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//div[@class="contentWarp710"]/table')[0]
                ca_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[2]//text()')))
                pro_name = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[2]//text()')))
                sale_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[5]/td[2]//text()')))[:-1]
                company = re.sub(r'\s', '', ''.join(table.xpath('.//tr[4]/td[2]//text()')))
                area = re.sub(r'\s', '', ''.join(table.xpath('.//tr[6]/td[2]//text()')))[:-2]
                ca_time = re.sub(r'-', '/', ca_time)
                pan_time = ''
                price = ''
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
            link = self.db.spop(self.redis_db)
            url = link.split('<<<')[0]
            ca_time = link.split('<<<')[1]
            num = self.parse_detail(url, ca_time)
            if num == 1:
                # time.sleep(1)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    p = Producer('GxGuilin:Detail')
    p.run()
    c = Consumer('GxGuilin:Detail')
    c.run()


if __name__ == '__main__':
    run()
