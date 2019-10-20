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
city = 'tianjing'


# 核发日期=发布日期
class Producer(TongyongSpider):
    url = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2019n/index_{}.html'
    url2 = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018/index_{}.html'
    url3 = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018_3441/index_{}.html'

    def get_links(self, url):
        response = requests.get(url, headers=self.headers)
        text = response.content.decode('utf-8')
        html = etree.HTML(text)
        table = html.xpath('//table[@class="table04"]')[0]
        trs = table.xpath('.//tr')[1:]
        hrefs = []
        for tr in trs:
            href = tr.xpath('./td[2]/a/@href')[0]
            hrefs.append(href[1:])
        return hrefs

    def run(self):
        urls1 = [self.url.format(i) for i in range(1, 38)] + ['http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2019n/index.html']
        for url in urls1:
            hrefs = self.get_links(url)
            for href in hrefs:
                link = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2019n' + href
                print(link)
                self.db.sadd(self.redis_db, link)
        urls2 = [self.url2.format(i) for i in range(1, 107)] + ['http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018/index.html']
        for url in urls2:
            hrefs = self.get_links(url)
            for href in hrefs:
                link = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018' + href
                print(link)
                self.db.sadd(self.redis_db, link)
        urls3 = [self.url3.format(i) for i in range(1, 663)] + ['http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018_3441/']
        for url in urls3:
            hrefs = self.get_links(url)
            for href in hrefs:
                link = 'http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2018_3441' + href
                print(link)
                self.db.sadd(self.redis_db, link)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                ca_time = html.xpath('//div[@class="con_Info"]/span[3]/text()')[0][3:]
                ca_time = re.sub(r'-', '/', ca_time)
                table = html.xpath('//table[@class="spfxsxk"]')[0]
                pro_name = table.xpath('.//tr[1]/td[2]/text()')[0]
                ca_num = ''.join(table.xpath('.//tr[2]/td[2]//text()'))
                ca_num = re.sub(r'\s', '', ca_num)
                company = re.sub(r'\s', '', ''.join(table.xpath('.//tr[3]/td[2]//text()')))
                area = table.xpath('.//tr[6]/td[2]/text()')[0]
                pan_time = ''
                price = ''
                sale_num = ''
                position = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception as e:
                print(url, e)
                if i == 4:
                    return 1

    def run(self):
        while True:
            set_num = self.db.scard(self.redis_db)
            if set_num == 0:
                print('数目为0')
                time.sleep(10)
                set_num2 = self.db.scard(self.redis_db)
                if set_num2 == 0: return
            link = self.db.spop(self.redis_db)
            num = self.parse_detail(link)
            if num == 1:
                time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, link)

def run():
    p = Producer('Tianjing:Detail')
    p.run()
    c = Consumer('Tianjing:Detail')
    c.run()


if __name__ == '__main__':
    run()