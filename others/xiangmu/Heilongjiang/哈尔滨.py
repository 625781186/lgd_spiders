# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import time
import datetime
from common.update_mongo import Update
from common.update_mongo import Update2

city='haerbin'
now = datetime.datetime.now().strftime('%Y/%m/%d')

url = 'http://47.104.94.71/ui/webSite/preSaleChange'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
first = {
    'year': '2005',
    'month': '7'
}
data = [{'year': '{}'.format(i), 'month': '7'} for i in range(2005, 2020)]


def parse_index(url, form_data):
    for i in range(1,5):
        try:
            response = requests.post(url, headers=headers, data=form_data)
            text = response.text
            html = etree.HTML(text)
            tables = html.xpath('//table')[:-1]
            for table in tables:
                test_info = ''.join(table.xpath('.//text()'))
                if '该城市本月暂无预售信息录入' not in test_info:
                    trs = table.xpath('.//tr')[1:]
                    for tr in trs:
                        build_name = ''.join(tr.xpath('.//td[1]/text()'))
                        pro_name = ''.join(tr.xpath('.//td[2]/a/text()'))
                        company = ''.join(tr.xpath('.//td[4]//text()'))
                        area = ''.join(tr.xpath('.//td[7]/text()'))
                        sale_num = ''.join(tr.xpath('.//td[8]/text()'))
                        ca_num = ''.join(tr.xpath('.//td[9]/text()'))
                        ca_time = ''.join(tr.xpath('.//td[10]/text()'))
                        ca_time = re.search(r'(\d+-\d+-\d+)', ca_time)
                        ca_time = ca_time.group(1) if ca_time else ''
                        ca_time=re.sub(r'-','/',ca_time)
                        url = 'http://47.104.94.71/ui/webSite/preSale2'
                        pan_time = ''
                        price = ''
                        position=build_name
                        build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                        print(build)
                        Update2(build, city)
            return
        except Exception as e:
            print(e)


def run():
    for form_data in data:
        parse_index(url, form_data)
        time.sleep(1)


if __name__ == '__main__':
    run()
