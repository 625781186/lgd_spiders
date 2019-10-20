# -*- coding: utf-8 -*-
import requests
import time
from lxml import etree
import re
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'zhuhai'


class ZhuhaiSpider(TongyongSpider):
    url = 'http://fdcjg.zhzgj.gov.cn/presalelist?keywords=presale&tabkey=all&searchcode=&start={}&count=30'

    def get_links(self, url):
        response = requests.get(url, headers=self.headers,timeout=40)
        text = response.text
        html = etree.HTML(text)
        lis = html.xpath('//div[@class="pub-list"]/ul/li')
        links = []
        for li in lis:
            href = li.xpath('./a/@href')[0]
            link = 'http://fdcjg.zhzgj.gov.cn' + href
            links.append(link)
        return links

    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//div[@class="building-info-table"]//table')[0]
                sale_num = table.xpath('.//tr[3]/td[4]/text()')[0]
                sale_num = re.sub(r'套', '', sale_num)
                company = ''.join(table.xpath('.//tr[2]/td[2]//text()'))
                area = table.xpath('.//tr[3]//td[2]/text()')[0][:-3]
                pro_name = html.xpath('//strong/text()')[0]
                ca_info = ''.join(html.xpath('//select[@id="presalepermitid"]/option[1]//text()'))
                ca_time = re.search(r'(\d+-\d+-\d+)', ca_info).group(1)
                ca_num = re.split('[（：）]', ca_info)[0]
                position = ','.join(html.xpath('//select[@id="buildnum"]//text()'))
                position=re.sub(r'\s','',position)
                pan_time = ''
                price = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return
            except Exception as e:
                print(url, e)
                if i == 4: return

    def run(self):
        for i in range(1,3):
            links = self.get_links(self.url.format(i))
            for link in links:
                self.parse_detail(link)
                time.sleep(3)


def run():
    obj = ZhuhaiSpider('GdZhuhai')
    obj.run()


if __name__ == '__main__':
    run()
