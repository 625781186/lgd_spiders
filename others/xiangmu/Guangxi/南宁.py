# -*- coding: utf-8 -*-
from lxml import etree
import re
import time
from selenium import webdriver
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'nanning'


# 网站很卡
class NanningSpider(TongyongSpider):
    url = 'http://gs.nnfcxx.com/index.php?s=/home1/index/sel/postid/%E5%95%86%E5%93%81%E6%88%BF.html'

    def __init__(self, redis_db):
        super(NanningSpider, self).__init__(redis_db)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def get_links(self):
        for i in range(1, 10):
            try:
                self.driver.get(self.url)
                text = self.driver.page_source
                html = etree.HTML(text)
                a_list = html.xpath('//div[@class="content"]//a')
                links = []
                for a in a_list:
                    href = a.xpath('./@href')[0]
                    link = 'http://gs.nnfcxx.com' + href
                    price = ''.join(a.xpath('.//div[2]/span[2]//text()'))
                    price = re.sub(r'元/㎡', '', price)
                    links.append(link + '<<<' + price)
                return links
            except Exception  as e:
                print(e)

    def parse_detail(self, url, price):
        for i in range(1, 10):
            try:
                self.driver.get(url)
                time.sleep(10)
                source = self.driver.page_source
                html = etree.HTML(source)
                content1 = html.xpath('//div[@class="content BasicInfo"]')[0]
                company = ''.join(content1.xpath('.//p[1]//text()'))
                company = re.sub(r'开发企业：', '', company)
                pro_name = content1.xpath('./p[2]/text()')[0][5:]
                content2 = html.xpath('//div[@class="content otherinfo"]')[1]
                sale_num = content2.xpath('.//li[1]/p[2]/text()')[0]
                content3 = html.xpath('//div[@class="content otherinfo"]')[1]
                ca_num = ''.join(content3.xpath('./div[@class="zheng"]//text()'))
                ca_num = re.sub(r'预售证号：', '', ca_num)
                pan_time = ''
                area = ''
                position = ''
                ca_time = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception as e:
                print(url, e)

    def run(self):
        links = self.get_links()
        for link in links:
            url = link.split('<<<')[0]
            price = link.split('<<<')[1]
            self.parse_detail(url, price)
        self.driver.close()


def run():
    obj = NanningSpider('GxNanning:Detail')
    obj.run()


if __name__ == '__main__':
    run()
