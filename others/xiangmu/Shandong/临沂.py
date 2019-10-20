# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import re
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'linyi'


class Consumer(TongyongSpider):
    url = 'http://shuju.lyzhujia.com/yushouchaxun?page={}'

    def parse_page(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                trs = html.xpath('//table[@class="match-table"]//tr')[1:]
                for tr in trs:
                    pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                    company = re.sub(r'\s', '', ''.join(tr.xpath('./td[5]//text()')))
                    ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[3]//text()')))
                    ca_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[1]//text()')))
                    ca_time = re.sub(r'-', '/', ca_time)
                    sale_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[6]//text()')))
                    area = re.sub(r'\s', '', ''.join(tr.xpath('./td[7]//text()')))
                    position = re.sub(r'\s', '', ''.join(tr.xpath('./td[8]//text()')))
                    pan_time = ''
                    price = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                return
            except Exception as e:
                print(url, e)

    def run(self):
        for i in range(1, 134):
            self.parse_page(self.url.format(i))
            time.sleep(1)


def run():
    c = Consumer('SdLinyi:Detail')
    c.run()


if __name__ == '__main__':
    run()
