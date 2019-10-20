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
city = 'baotou'


class Producer(TongyongSpider):
    def __init__(self, redis_db):
        super(Producer, self).__init__(redis_db)
        self.url = 'http://zfhcxjsj.baotou.gov.cn/permit/current_page/{}.jsp'

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table[@style="background-color:#fff; margin:0 auto;"]')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    href = tr.xpath('./td[2]/a/@href')[0]
                    link = 'http://zfhcxjsj.baotou.gov.cn' + href
                    print(link)
                    self.db.sadd(self.redis_db, link)
            except Exception as e:
                print(url, e)

    def run(self):
        for i in range(1, 52):
            self.get_links(self.url.format(i))
            time.sleep(0.2)


class Consumer(TongyongSpider):
    def __init__(self, redis_db):
        super(Consumer, self).__init__(redis_db)

    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//div[@class="PermitTable"]//table')[0]
                ca_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[2]//text()')))
                ca_time = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[4]//text()')))
                ca_time = re.sub(r'[-.年月]', '/', ca_time)
                ca_time = re.sub(r'日', '', ca_time)
                company = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[2]//text()')))
                pro_name = re.sub(r'\s', '', ''.join(table.xpath('.//tr[3]/td[2]//text()')))
                sale_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[6]/td[2]//text()')))
                sale_num = re.search(r'(\d+)套', sale_num)
                sale_num = sale_num.group(1) if sale_num else ''
                area = re.sub(r'\s', '', ''.join(table.xpath('.//tr[6]/td[3]//text()')))
                area = re.sub(r'㎡', '', area)
                pan_time = re.sub(r'\s', '', ''.join(table.xpath('.//tr[11]/td[2]//text()')))
                pan_time = re.sub(r'[-.年月]', '/', pan_time)
                pan_time = re.sub(r'日', '', pan_time)
                price = ''
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
            href = self.db.spop(self.redis_db)
            num = self.parse_detail(href)
            if num == 1:
                time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, href)


def run():
    p = Producer('NmBaotou:Detail')
    p.run()
    c = Consumer('NmBaotou:Detail')
    c.run()


if __name__ == '__main__':
    run()
