# -*- coding: utf-8 -*-
from selenium import webdriver
from lxml import etree
import re
import time
import datetime
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'zhaoqing'


class Producer(TongyongSpider):
    url = 'http://61.146.213.163:8011/New_pre.aspx?lid=%7BF96EA453-7C8F-488C-BEB4-A696849BBA06%7D&code=441202&page={}'

    def __init__(self, redis_db):
        super(Producer, self).__init__(redis_db)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def get_links(self, url):
        for i in range(1, 5):
            try:
                print(url)
                self.driver.get(url)
                time.sleep(1)
                source = self.driver.page_source
                html = etree.HTML(source)
                table = html.xpath('//table[@id="table1"]')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    href = tr.xpath('./td[2]/a/@href')[0]
                    ca_num = ''.join(tr.xpath('./td[2]/a//text()'))
                    position = ''.join(tr.xpath('./td[5]//text()'))
                    link = 'http://61.146.213.163:8011/' + href
                    self.db.sadd(self.redis_db, link + '<<<' + ca_num + '<<<' + position)
                return
            except Exception as e:
                print(url, e)

    def run(self):
        for i in range(1, 12):
            url = self.url.format(i)
            self.get_links(url)
        self.driver.close()


class Consumer(TongyongSpider):
    def __init__(self, redis_db):
        super(Consumer, self).__init__(redis_db)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def parse_detail(self, url, ca_num, position):
        for i in range(1,5):
            try:
                self.driver.get(url)
                time.sleep(1)
                source = self.driver.page_source
                html = etree.HTML(source)
                company = ''.join(html.xpath('//font[@id="kfsmc"]//text()'))
                pro_name = ''.join(html.xpath('//font[@id="PresellName"]//text()'))
                ca_time = ''.join(html.xpath('//font[@id="FZDate"]//text()'))
                ca_time = re.search(r'(\d+年\d+月\d+)日', ca_time)
                ca_time = ca_time.group(1) if ca_time else ''
                ca_time = re.sub(r'[年月日]', '/', ca_time)
                sale_info = ''.join(html.xpath('//font[@id="PresellArea"]//text()'))
                area = re.search(r'(.*?)平方米', sale_info)
                area = area.group(1) if area else ''
                sale_num = re.search(r'(\d+)套', sale_info)
                sale_num = sale_num.group(1) if sale_num else ''
                pan_time = ''
                price = ''
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
            url = link.split('<<<')[0]
            ca_num = link.split('<<<')[1]
            position = link.split('<<<')[2]
            num = self.parse_detail(url, ca_num, position)
            if num == 1:
                # time.sleep(1)
                pass
            else:
                self.db.sadd(self.redis_db, link)

def run():
    p = Producer('GdZhaoqing:Detail')
    p.run()
    c = Consumer('GdZhaoqing:Detail')
    c.run()


if __name__ == '__main__':
    run()