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
city='luoyang'
#会卡一下，自动化的时候去找一下问题
# 有频率限制
class Producer(TongyongSpider):
    url = 'http://123.7.180.231/bit-xxzs/xmlpzs/prewebissue.asp?page={}'

    def get_links(self, url):
        for i in range(1,5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('gbk')
                html = etree.HTML(text)
                table = html.xpath('//form[@id]/following-sibling::table')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    href = tr.xpath('./td[1]/a/@href')[0]
                    link = 'http://123.7.180.231/bit-xxzs/xmlpzs/' + href
                    ca_time = ''.join(tr.xpath('./td[last()]//text()'))
                    print(link)
                    self.db.sadd(self.redis_db, link + '<<<' + ca_time)
            except Exception as e:
                print(e)

    def run(self):
        for i in range(1, 112):
            url = self.url.format(i)
            self.get_links(url)
            time.sleep(4)


class Consumer(TongyongSpider):
    def parse_detail(self, url, ca_time):
        try:
            print(url)
            ca_time=re.sub(r'-','/',ca_time)
            response = requests.get(url, headers=self.headers,timeout=40)
            text = response.content.decode('gbk')
            html = etree.HTML(text)
            table0 = html.xpath(
                '//table[@style="BORDER-RIGHT: #9CC7FA 1px solid; BORDER-TOP: #9CC7FA 1px solid; BORDER-LEFT: #9CC7FA 1px solid; BORDER-BOTTOM: #9CC7FA 1px solid"]')[
                0]
            company = ''.join(table0.xpath('.//tr[2]/td[2]//text()'))
            pro_name = ''.join(table0.xpath('.//tr[3]/td[2]//text()'))
            area = ''.join(table0.xpath('.//tr[4]/td[2]//text()'))
            ca_num = ''.join(table0.xpath('.//tr[9]/td[2]//text()'))
            table1 = html.xpath(
                '//table[@style="BORDER-RIGHT: #9CC7FA 1px solid; BORDER-TOP: #9CC7FA 1px solid; BORDER-LEFT: #9CC7FA 1px solid; BORDER-BOTTOM: #9CC7FA 1px solid"]')[
                1]
            trs = table1.xpath('.//tr')[1:]
            if len(trs) > 0:
                positions = []
                sale_num = 0
                for tr in trs:
                    detail_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[3]//text()')))
                    if detail_num:
                        sale_num += int(detail_num)
                    locate = ''.join(tr.xpath('./td[2]//text()'))
                    positions.append(locate)
                position = ','.join(positions)
                pan_time = ''
                price = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
            else:
                pan_time = ''
                price = ''
                sale_num=''
                position=''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
            return 1
        except Exception as e:
            print(url,e)
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
            link = href.split('<<<')[0]
            ca_time = href.split('<<<')[1]
            num = self.parse_detail(link, ca_time)
            if num == 1:
                time.sleep(2)
                pass
            else:
                self.db.sadd(self.redis_db, href)


def run():
    obj = Producer('HnLuoyang:Detail')
    obj.run()
    c = Consumer('HnLuoyang:Detail')
    c.run()

if __name__ == '__main__':
    run()
