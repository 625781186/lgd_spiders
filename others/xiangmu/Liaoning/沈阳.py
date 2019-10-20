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
city = 'shenyang'


# 只有一页，网页响应很慢，多尝试几次
# 住宅栋号
class Producer(TongyongSpider):
    max_page = 415
    url = 'http://www.syfc.com.cn/work/ysxk/query_xukezheng.jsp?cur_page={}'

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                a_list = html.xpath('//a')
                for a in a_list:
                    if '查看详细' in ''.join(a.xpath('.//text()')):
                        link = 'http://www.syfc.com.cn' + a.xpath('./@href')[0]
                        print(link)
                        self.db.sadd(self.redis_db, link)
            except Exception as e:
                print(e)

    def run(self):
        for i in range(1, self.max_page):
            self.get_links(self.url.format(i))
            time.sleep(0.2)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table')[1]
                position = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[4]//text()')))
                company = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[2]//text()')))
                sale_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[5]/td[4]//text()')))
                area = re.sub(r'\s', '', ''.join(table.xpath('.//tr[6]/td[2]//text()')))
                ca_time = re.sub(r'\s', '', ''.join(table.xpath('.//tr[9]/td[4]//text()')))
                ca_time = re.sub(r'-', '/', ca_time)
                ca_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[10]/td[4]//text()')))
                beizhu = re.sub(r'\s', '', ''.join(table.xpath('.//tr[11]/td[2]//text()')))
                position = beizhu if ('见备注' in position) else position
                pan_time = ''
                price = ''
                pro_name = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception:
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
                time.sleep(0.7)
                pass
            else:
                self.db.sadd(self.redis_db, href)

def run():
    p = Producer('LnShenyang:Detail')
    p.run()
    c = Consumer('LnShenyang:Detail')
    c.run()

if __name__ == '__main__':
    run()
