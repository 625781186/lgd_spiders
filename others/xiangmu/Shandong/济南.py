# -*- coding: utf-8 -*-
from common.spider_class import TongyongSpider
import requests
from lxml import etree
from common.update_mongo import Update
from common.update_mongo import Update2
import re
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'jinan'


class Consumer(TongyongSpider):
    first_url = 'http://jncc.jinan.gov.cn/jncjzhcx/zhcx/spfysxkz.do?searchname=xmmc&searchword=%E5%BC%80%E5%8F%91%E9%A1%B9%E7%9B%AE'
    url = 'http://jncc.jinan.gov.cn/jncjzhcx/zhcx/spfysxkz.do?ym={}&method=1&searchname=xmmc&searchword=%E5%BC%80%E5%8F%91%E9%A1%B9%E7%9B%AE'

    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[1]//text()')))
                    company = re.sub(r'\s', '', ''.join(tr.xpath('./td[2]//text()')))
                    pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                    position = re.sub(r'\s', '', ''.join(tr.xpath('./td[5]//text()')))
                    ca_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[8]//text()')))
                    ca_time = re.sub(r'-', '/', ca_time)
                    pan_time = ''
                    price = ''
                    sale_num = ''
                    area = ''
                    # build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    # print(build)
                    # Update2(build, city)

                    # print(ca_num)
                    # print(ca_time)
                    # print(pro_name)
                    # print(jianshe_unit)
                    # print(pro_position)
                    # print(pro_guimo)
                    # print(region)
                    # print(spider_time)
                    # print(link_url)

                return
            except Exception as e:
                print(url, e)

    def run(self):
        for i in range(1, 101):
            self.parse_detail(self.url.format(i))


def run():
    c = Consumer('SdJinan:Detail')
    c.run()


if __name__ == '__main__':
    run()
