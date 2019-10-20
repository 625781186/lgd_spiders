# -*- coding: utf-8 -*-
from selenium import webdriver
from lxml import etree
import re
import time
import pymongo
from common.update_mongo import Update2
import datetime

city = 'huizhou'
now = datetime.datetime.now().strftime('%Y/%m/%d')


# 需要用selenium,71页会挂掉，手动换到72页
class HuizhouSpider():
    url = 'http://113.106.199.148/web/salepermit.jsp?page={}&projectname=&code=&compname=&&address=&date1=&date2='
    client = pymongo.MongoClient('mongodb://root:123456@127.0.0.1:27017')

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def parse_detail(self, url):
        try:
            print(url)
            self.driver.get(url)
            time.sleep(0.5)
            for i in range(2, 17):
                a = self.driver.find_element_by_xpath('//div[@class="answer"]//tr[%s]/td[2]/a' % i)
                company = self.driver.find_element_by_xpath('//div[@class="answer"]//tr[%s]/td[4]' % i)
                company = re.sub(r'\s', '', company.text)
                try:
                    a.click()
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    time.sleep(0.7)
                    source = self.driver.page_source
                    html = etree.HTML(source)
                    table = html.xpath('//div[@class="Searchbox"]/table')[0]
                    ca_num = re.sub(r'\s', '', table.xpath('.//tr[1]/td/text()')[0])
                    pro_name = re.sub(r'\s', '', table.xpath('.//tr[3]/td/text()')[0])
                    area = re.sub(r'\s', '', table.xpath('.//tr[6]/td[1]/text()')[0])[:-1]
                    sale_num = re.sub(r'\s', '', table.xpath('.//tr[6]/td[2]/text()')[0])
                    position = re.sub(r'\s', '', table.xpath('.//tr[7]/td[2]/text()')[0])
                    ca_time = re.sub(r'\s', '', table.xpath('.//tr[last()-2]/td[2]/text()')[0])
                    ca_time = re.sub(r'-', '/', ca_time)
                    pan_time = ''
                    price = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                except Exception as e:
                    print(url, '某个详细地址有异常')
        except Exception as e:
            print(url, e)

    def run(self):
        self.driver.get('https://www.baidu.com')
        for i in range(1, 103):
            self.parse_detail(self.url.format(i))
        self.driver.close()


def run():
    obj = HuizhouSpider()
    obj.run()


if __name__ == '__main__':
    run()
