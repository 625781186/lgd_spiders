# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import time
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'handan'


class Consumer(TongyongSpider):
    url = 'http://www.ljia.net/zt2013/0313//?p={}'

    def parse_page(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                table = html.xpath('//table')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[1]//text()')))
                    pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[2]//text()')))
                    position = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                    company = re.sub(r'\s', '', ''.join(tr.xpath('./td[5]//text()')))
                    ca_time = ''
                    pan_time = ''
                    sale_num = ''
                    area = ''
                    price = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                return
            except Exception as e:
                print(e)

    def run(self):
        urls = [self.url.format(i) for i in range(1, 121)]
        for url in urls:
            self.parse_page(url)


def run():
    c = Consumer('HbHandan:Detail')
    c.run()


if __name__ == '__main__':
    run()
