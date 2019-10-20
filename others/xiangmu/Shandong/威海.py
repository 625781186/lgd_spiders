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
city = 'weihai'


# 有时候会卡住，以后再找问题
class Consumer(TongyongSpider):
    url = 'http://www.whhouse.com/index.php?m=content&c=index&a=lists&catid=155&page={}'

    def parde_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    title = re.sub(r'\s', '', ''.join(tr.xpath('./td[1]//text()')))
                    position = re.sub(r'\s', '', ''.join(tr.xpath('./td[2]//text()')))
                    ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[3]//text()')))
                    ca_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                    ca_time = re.sub(r'-', '/', ca_time)
                    try:
                        pro_name = title if title else pro_name
                        pan_time = ''
                        price = ''
                        sale_num = ''
                        area = ''
                        company = ''
                        build = (
                        pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                        print(build)
                        Update2(build, city)
                    except UnboundLocalError:
                        print('抛弃这条')
                return
            except Exception as e:
                print(url, e)

    def run(self):
        for i in range(1, 52):
            self.parde_detail(self.url.format(i))
            time.sleep(1.5)


def run():
    c = Consumer('SdWeihai:Detail')
    c.run()


if __name__ == '__main__':
    run()
