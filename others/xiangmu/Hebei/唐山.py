# -*- coding: utf-8 -*-
import requests
from lxml import etree
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import re
import time
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city='tangshan'

class Producer(TongyongSpider):
    def __init__(self, redis_db):
        super(Producer, self).__init__(redis_db)
        self.url = 'http://zhujianjujk.tangshan.gov.cn/wsyscx.jspx?pageNo={}&type=&typeval='

    def get_links(self, url):
        for i in range(1,5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table[@style="border-collapse:collapse"]')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    href = tr.xpath('.//a[1]/@href')[0]
                    link = 'http://zhujianjujk.tangshan.gov.cn' + href
                    print(link)
                    self.db.sadd(self.redis_db, link)
            except Exception as e:
                print(e)

    def run(self):
        for i in range(1, 251):
            self.get_links(self.url.format(i))


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1,5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('utf-8')
                if "页面找不到" in text: return 1
                html = etree.HTML(text)
                table = html.xpath('//table[@style="border-collapse:collapse; margin-top:10px;"]')[0]
                ca_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[2]//text()')))
                company = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[4]//text()')))
                pro_name = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[2]//text()')))
                area = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[4]//text()')))
                sale_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[3]/td[4]//text()')))
                ca_time = re.sub(r'\s', '', ''.join(table.xpath('.//tr[4]/td[2]//text()')))
                ca_time = re.search(r'(\d+-\d+-\d+)', ca_time)
                ca_time = ca_time.group(1) if ca_time else ''
                ca_time = re.sub(r'-', '/', ca_time)
                position = re.sub(r'\s', '', ''.join(table.xpath('.//tr[4]/td[4]//text()')))
                pan_time = ''
                price = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception:
                print(url, '解析异常')
                if i==4:
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
                time.sleep(0.2)
                pass
            else:
                self.db.sadd(self.redis_db, href)

def run():
    p = Producer('HbTangshan:Detail')
    p.run()
    c = Consumer('HbTangshan:Detail')
    c.run()

if __name__ == '__main__':
    run()
