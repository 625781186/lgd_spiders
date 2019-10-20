# -*- coding: utf-8 -*-
from common.spider_class import TongyongSpider
import requests
from lxml import etree
import re
from common.update_mongo import Update
from common.update_mongo import Update2
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'qingzhou'


# 网站很烂，多试几次
class Consumer(TongyongSpider):
    url = 'http://218.59.129.50:808/bvdfweb/iNetInfoAction!preSellInfo.action?flag=topresell'
    data = {'pageNo': '1', 'pageSize': '1420', 'colName': 'corpName'}

    def parse_zoom(self):
        for i in range(1, 5):
            try:
                response = requests.post(self.url, headers=self.headers, data=self.data,timeout=40)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                trs = html.xpath('//table[@class="table03"]//tr')[1:]
                for tr in trs:
                    company = re.sub(r'\s', '', ''.join(tr.xpath('./td[2]//text()')))
                    pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[3]//text()')))
                    position = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                    ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[6]//text()')))
                    ca_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[7]//text()')))
                    ca_time = re.sub(r'-', '/', ca_time)
                    pan_time = ''
                    price = ''
                    area = ''
                    sale_num = ''
                    build = (
                    pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, self.url)
                    print(build)
                    Update2(build, city)
                return
            except Exception as e:
                print(e)


def run():
    c = Consumer('SdQingzhou:Detail')
    c.parse_zoom()


if __name__ == '__main__':
    run()
