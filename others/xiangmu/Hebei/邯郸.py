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
city = 'handan'


class Producer(TongyongSpider):
    url = 'http://www.ljia.net/zt2013/0313//?p={}'

    def parse_page(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                table = html.xpath('//table')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    href = tr.xpath('./td[2]/a/@href')[0]
                    link = 'http://www.ljia.net' + href
                    ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[1]//text()')))
                    pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[2]//text()')))
                    position = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                    company = re.sub(r'\s', '', ''.join(tr.xpath('./td[5]//text()')))
                    print(link, ca_num)
                    self.db.sadd(self.redis_db,
                                 link + '<<<' + ca_num + '<<<' + pro_name + '<<<' + position + '<<<' + company)
                return
            except Exception as e:
                print(e)

    def run(self):
        urls = [self.url.format(i) for i in range(1, 121)]
        for url in urls:
            self.parse_page(url)
            time.sleep(1)


class Consumer(TongyongSpider):
    def parse_detail(self, url, ca_num, pro_name, position, company):
        for i in range(1, 5):
            try:
                if 'http://www.ljia.netjavascript' in url:
                    ca_time=''
                    pan_time=''
                    sale_num=''
                    area=''
                    price=''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print('这条去除')
                    Update2(build, city)
                    return 1
                response = requests.get(url, headers=self.headers)
                if response.status_code == 404: return 1
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                pan_time = re.sub(r'\s', '', ''.join(html.xpath('//div[@class="w730 r por"]/dl[3]/dd//text()')))
                pan_time = re.sub(r'[年月]', '/', pan_time)
                pan_time = re.sub(r'日', '', pan_time)
                price = re.sub(r'\s', '', ''.join(html.xpath('//i[@id="pri"]//text()')))
                price = re.sub(r'元/平米', '', price)
                area = ''.join(html.xpath('//div[@class="houseDesc"]/p[4]/span[2]//text()'))
                area = re.search(r'(\d+\.?\d+)㎡', area)
                area = area.group(1) if area else ''
                sale_tag = html.xpath('//div[@class="houseDesc"]/p[@class="line"]')[5]
                sale_num = ''.join(sale_tag.xpath('./span[1]//text()'))
                sale_num = re.search(r'(\d+)', sale_num)
                sale_num = sale_num.group(1) if sale_num else ''
                ca_time = ''
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
            url = link.split('<<<')[0]
            print(url)
            ca_num = link.split('<<<')[1]
            pro_name = link.split('<<<')[2]
            position = link.split('<<<')[3]
            company = link.split('<<<')[4]
            num = self.parse_detail(url, ca_num, pro_name, position, company)
            if num == 1:
                time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    p = Producer('HbHandan:Detail')
    p.run()
    c = Consumer('HbHandan:Detail')
    c.run()


if __name__ == '__main__':
    run()
