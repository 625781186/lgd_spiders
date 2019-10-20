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
city = 'kunming'


class KunmingSpider(TongyongSpider):
    url = 'http://www.kmhouse.org/lqt/SellLicenseDisp.asp'

    def parse_detail(self, url, data):
        for i in range(1, 5):
            try:
                num = data['thePage']
                response = requests.post(url, headers=self.headers, data=data)
                text = response.content.decode('gbk')
                html = etree.HTML(text)
                tables = html.xpath('//table[@align="Left"]')
                for table in tables:
                    pro_name = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td//text()'))[5:])
                    company = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[2]//text()')))
                    company = re.sub(r'开发商：', '', company)
                    ca_time = re.sub(r'\s', '', ''.join(table.xpath('.//tr[4]/td[1]//text()'))[5:])
                    ca_time = re.sub(r'-', '/', ca_time)
                    ca_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[3]/td[2]//text()'))[7:])
                    area = re.sub(r'\s', '', ''.join(table.xpath('.//tr[4]/td[2]//text()'))[5:])
                    area = re.sub(r'㎡', '', area)
                    pan_time = ''
                    price = ''
                    sale_num = ''
                    position = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                return
            except Exception as e:
                print(url, e)
def run():
    obj = KunmingSpider('YnKunming:Detail')
    for i in range(1, 204):
        da = {'thePage': '{}'.format(i)}
        obj.parse_detail('http://www.kmhouse.org/lqt/SellLicenseDisp.asp', da)
        time.sleep(2)


if __name__ == '__main__':
   run()
