# -*- coding: utf-8 -*-
import requests
import re
import time
from lxml import etree
import datetime
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'zibo'


class Producer(TongyongSpider):
    def __init__(self, redis_db):
        super(Producer, self).__init__(redis_db)
        self.url = 'http://www.zbfdc.com.cn/web/building/list?page={}'

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                a_list = html.xpath('//ul[@class="list"]//li//a/@href')
                for a in a_list:
                    print(a)
                    self.db.sadd(self.redis_db, a)
                return
            except Exception as e:
                print(url, e)

    def run(self):
        for i in range(1, 705):
            self.get_links(self.url.format(i))
            time.sleep(0.5)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                if response.text == '{"success":false,"fieldErrors":null,"msg":"楼盘下无房屋","data":null}': return 1
                html = etree.HTML(text)
                position = re.sub(r'\s', '', ''.join(html.xpath('//div[@class="building-title"]//text()')))
                ul = html.xpath('//ul[@class="clearfix"]')[0]
                pro_name = re.sub(r'\s', '', ''.join(ul.xpath('./li[1]/span[2]//text()')))
                company = re.sub(r'\s', '', ''.join(ul.xpath('./li[7]/span[2]//text()')))
                area = re.sub(r'\s', '', ''.join(ul.xpath('./li[8]/span[2]//text()')))
                ca_num = re.sub(r'\s', '', ''.join(ul.xpath('./li[9]/span[2]//text()')))
                sale_num = re.sub(r'\s', '', ''.join(ul.xpath('./li[10]/span[2]//text()')))
                yongdi_time = re.sub(r'\s', '', ''.join(ul.xpath('./li[2]/span[2]//text()')))
                yongdi_time = re.search(r'(20\d\d)', yongdi_time)
                yongdi_time = yongdi_time.group(1) if yongdi_time else ''
                gongcheng_time = re.sub(r'\s', '', ''.join(ul.xpath('./li[4]/span[2]//text()')))
                gongcheng_time = re.search(r'(20\d\d)', gongcheng_time)
                gongcheng_time = gongcheng_time.group(1) if gongcheng_time else ''
                pan_time = ''
                price = ''
                ca_time = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception:
                print('解析详情页异常')
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
    p = Producer('SdZibo:Detail')
    p.run()
    c = Consumer('SdZibo:Detail')
    c.run()


if __name__ == '__main__':
    run()
