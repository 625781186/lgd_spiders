# -*- coding: utf-8 -*-
import requests
import time
import re
import json
from common.spider_class import TongyongSpider
from common.update_mongo import Update
from common.update_mongo import Update2
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'yantai'
url = 'http://www.ytfcjy.com:2019/CMS/SPF/GetYSXKList?startno={0}&endno={1}&value=%7B%22District%22%3A%22%E6%89%80%E6%9C%89%E5%8C%BA%E5%9F%9F%22%2C%22Code%22%3A%22%22%2C%22ProjectName%22%3A%22%22%7D'
urls = [url.format(i, i + 20) for i in range(0, 960, 20)]


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                data = json.loads(text)['rows']
                for i in data:
                    ca_num = i['CODE']
                    pro_name = i['PROJECTNAME']
                    company = i['COMPANY']
                    sale_num = i['SETS']
                    area = i['AREA']
                    ca_time = i['CARDDATE']
                    ca_time = ca_time.split(r' ')[0]
                    pan_time = ''
                    price = ''
                    position = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                return
            except Exception as e:
                print(url, e)

    def run(self):
        for url in urls:
            self.parse_detail(url)
            time.sleep(1)


def run():
    c = Consumer('SdYantai:Detail')
    c.run()


if __name__ == '__main__':
    run()
