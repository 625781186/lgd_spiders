# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import time
import datetime
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'zhoukou'


class ZhoukouSpider(TongyongSpider):
    url = 'http://www.zkzj.gov.cn/Home/NewsList?Id=2900&curr=34&pageindex={}'

    def get_link(self, url):
        response = requests.get(url, headers=self.headers,timeout=40)
        text = response.text
        html = etree.HTML(text)
        a_list = html.xpath('//ul[@class="newslist"]//a')
        links = []
        for a in a_list:
            title = a.xpath('./text()')[0]
            href = a.xpath('./@href')[0]
            href = 'http://www.zkzj.gov.cn' + href
            if '许可证' in title:
                links.append(href)
        return links

    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table')[0]
                pro_name = ''.join(table.xpath('.//tr[1]/td[2]//text()'))
                pro_name = re.sub(r'\s', '', pro_name)
                company = ''.join(table.xpath('.//tr[1]/td[4]//text()'))
                company = re.sub(r'\s', '', company)
                area = ''.join(table.xpath('.//tr[3]/td[2]//text()'))
                position = ''.join(table.xpath('.//tr[3]/td[4]//text()'))
                position = re.sub(r'\s', '', position)
                ca_time = ''.join(table.xpath('.//tr[4]/td[2]//text()'))
                ca_time = re.sub(r'\.', '/', ca_time)
                ca_num = ''.join(html.xpath('//h1//text()'))
                ca_num = re.split('[（）]', ca_num)[1]
                pan_time = ''
                price = ''
                sale_num = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return
            except Exception as e:
                print(e)

    def run(self):
        urls = [self.url.format(i) for i in range(1, 3)]
        for x in urls:
            links = self.get_link(x)
            for link in links:
                self.parse_detail(link)
                time.sleep(1)


def run():
    obj = ZhoukouSpider('HnZhoukou:Detail')
    obj.run()


if __name__ == '__main__':
    run()
