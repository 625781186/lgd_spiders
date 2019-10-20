# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import re
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
from selenium import webdriver
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'yingkou'


class Producer(TongyongSpider):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')

    def __init__(self, redis_db):
        super(Producer, self).__init__(redis_db)
        self.url = 'http://sp.yingkou.gov.cn/002/about.html?categoryNum=002&pageIndex={}'
        self.driver = webdriver.Chrome(options=Producer.option)

    def get_links(self, url):
        for i in range(1, 5):
            try:
                self.driver.get(url)
                time.sleep(1)
                source = self.driver.page_source
                html = etree.HTML(source)
                lis = html.xpath('//ul[@id="infolist"]//li')
                for li in lis:
                    text = ''.join(li.xpath('.//text()'))
                    if '商品房预售公示' in text:
                        href = li.xpath('.//a/@href')[0]
                        link = 'http://sp.yingkou.gov.cn' + href
                        print(link)
                        self.db.sadd(self.redis_db, link)
            except Exception as e:
                print(e)

    def run(self):
        for i in range(1, 35):
            self.get_links(self.url.format(i))
        self.driver.close()


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                content = re.sub(r'\s', '', ''.join(html.xpath('//div[@id="ivs_content"]//text()')))
                pro_name = re.search(r'项目名称：(.*?)预售', content).group(1)
                company = re.search(r'(.*?公司)', content)
                company = company.group(1) if company else ''
                ca_num = re.search(r'预售许可证号：(.*?)项目', content).group(1)
                sale_num = re.search(r'销售套数：(.*?)销售', content).group(1)
                sale_num = re.search(r'(\d+)套', sale_num)
                sale_num = sale_num.group(1) if sale_num else ''
                area = re.search(r'销售面积：(.*?)开发', content).group(1)
                area = re.search(r'(\d+\.?\d+)㎡', area)
                area = area.group(1) if area else ''
                ca_time = re.search(r'(\d+年\d+月\d+日)', content)
                ca_time = ca_time.group(1) if ca_time else ''
                ca_time = re.sub(r'[年月]', '/', ca_time)
                ca_time = re.sub(r'日', '', ca_time)
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
            num = self.parse_detail(link)
            if num == 1:
                time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    p = Producer('LnYingkou:Detail')
    p.run()
    c = Consumer('LnYingkou:Detail')
    c.run()


if __name__ == '__main__':
    run()
