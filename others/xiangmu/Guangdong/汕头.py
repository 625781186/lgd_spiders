# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import time
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime
import os

path=os.path.dirname(__file__)
file='city.txt'

city = 'shantou'
now = datetime.datetime.now().strftime('%Y/%m/%d')


class ShantouSpider(TongyongSpider):
    url = 'http://125.91.12.242/stsite/Vendition/index.aspx'

    def get_links(self):
        response = requests.get(self.url, headers=self.headers,timeout=40)
        text = response.text
        html = etree.HTML(text)
        a_list = html.xpath('//a')
        links = []
        for a in a_list:
            href = a.xpath('./@href')[0]
            if ('ProjectList' in href) and ('presaleid' in href):
                link = 'http://125.91.12.242/stsite' + href[2:]
                links.append(link)
        return links

    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                ca_num = html.xpath('//span[@id="Prenum"]/text()')[0]
                pro_name = html.xpath('//span[@id="ProjectName"]/text()')[0]
                ca_time = html.xpath('//span[@id="Issued"]/text()')[0]
                sale_num = html.xpath('//span[@id="RoomCount"]/text()')[0]
                position = html.xpath('//span[@id="P_dhcs"]/text()')[0]
                area = html.xpath('//span[@id="TtlBarea"]/text()')[0]
                area = re.sub(r',', '', area)
                ca_time = re.sub(r'-', '/', ca_time)
                company = ''.join(html.xpath('//span[@id="CompanyName"]//text()'))
                pan_time = ''
                price = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return
            except Exception as e:
                print(url, e)
                if i == 4:
                    return

    def run(self):
        links = self.get_links()
        for link in links:
            self.parse_detail(link)
            time.sleep(2)


def run():
    try:
        obj = ShantouSpider('GdShantou')
        obj.run()
    except Exception as e:
        file_path=os.path.join(path,file)
        with open(file_path,'at',encoding='utf-8') as fp:
            fp.write(str(e))
            fp.write('\r')

if __name__ == '__main__':
    run()
