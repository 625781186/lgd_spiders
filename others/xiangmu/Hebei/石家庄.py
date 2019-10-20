# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import datetime
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'shijiazhuang'


class ShijiazhuangSpider(TongyongSpider):
    url = 'http://zjj.sjz.gov.cn/plus/scxx_ysxk.php?pageno={}&'

    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                tables = html.xpath('//table')[1:]
                for table in tables:
                    ca_num = table.xpath('.//tr[1]/td[2]/text()')[0]
                    company = table.xpath('.//tr[1]/td[1]/text()')[0]
                    pro_name = table.xpath('.//tr[3]/td/text()')[0]
                    position = table.xpath('.//tr[5]/td/text()')[0]
                    pan_time = ''
                    price = ''
                    sale_num = ''
                    ca_time = ''
                    area = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
            except Exception as e:
                print(e)

    def run(self):
        urls = [self.url.format(i) for i in range(1, 221)]
        for url in urls:
            self.parse_detail(url)
            time.sleep(1)


def run():
    obj = ShijiazhuangSpider('HbShijiazhuang:Detail')
    obj.run()


if __name__ == '__main__':
    run()
