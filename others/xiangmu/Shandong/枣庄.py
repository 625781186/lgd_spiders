# coding=utf-8
import requests
from lxml import etree
import time
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import re
import datetime
from selenium import webdriver

now = datetime.datetime.now().strftime('%Y/%m/%d')
city='zaozhuang'

# 要先拿到cookies
class Consumer(TongyongSpider):
    url = 'http://www.zaofang.net/yushou/list.php?type=1&page={}'

    def __init__(self, redis_db):
        super(Consumer, self).__init__(redis_db)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def parse_detail(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)
            source = self.driver.page_source
            html = etree.HTML(source)
            trs = html.xpath('//table//tr')[1:]
            for tr in trs:
                ca_time = tr.xpath('./td[1]//text()')[0]
                ca_time = re.sub(r'-', '/', ca_time)
                ca_num = tr.xpath('./td[3]//text()')[0]
                pro_name = tr.xpath('./td[4]//text()')[0]
                company = tr.xpath('./td[5]//text()')[0]
                area = tr.xpath('./td[6]//text()')[0]
                area = re.sub(r'㎡', '', area)
                pan_time = ''
                price = ''
                sale_num=''
                position=''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
        except Exception as e:
            print(e)

    def run(self):
        self.driver.get('https://www.baidu.com')
        for i in range(1, 5):
            self.parse_detail(self.url.format(i))
        self.driver.close()

def run():
    c = Consumer('SdZaoZhuang:Detail')
    c.run()

if __name__ == '__main__':
   run()
