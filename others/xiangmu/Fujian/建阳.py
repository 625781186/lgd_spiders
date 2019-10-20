# coding=utf-8
import requests
from lxml import etree
import re
import time
from common.spider_class import TongyongSpider
from common.update_mongo import Update2
import datetime
import os

path=os.path.dirname(__file__)
file='city.txt'

city = 'jianyang'
now = datetime.datetime.now().strftime('%Y/%m/%d')


# 有频率限制
class Producer(TongyongSpider):
    url = 'http://www.jyfdc.com/House/link/ListPreSell?pagenumber={}&pagesize=15&CantonID=15'

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=30)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    ca_time = ''.join(tr.xpath('./td[6]//text()'))
                    href = tr.xpath('.//td[7]/a/@href')[0]
                    link = 'http://www.jyfdc.com' + href
                    company = ''.join(tr.xpath('./td[3]//text()'))
                    print(link)
                    self.db.sadd(self.redis_db, link + '<<<' + ca_time + '<<<' + company)
                return
            except Exception as e:
                print(url, e)
                if i == 4: return

    def run(self):
        for i in range(1, 30):
            url = self.url.format(i)
            self.get_links(url)
            time.sleep(2)


class Consumer(TongyongSpider):
    def parse_detail(self, url, ca_time, company):
        try:
            response = requests.get(url, headers=self.headers, timeout=20)
            if response.status_code == 400:
                return 1
            text = response.text
            html = etree.HTML(text)
            table0 = html.xpath('//table')[0]
            if not table0:
                return 1
            pro_name = re.sub(r'\s', '', ''.join(html.xpath('//h3//text()')))[7:]
            ca_num = ''.join(table0.xpath('//tr[2]/td[1]//text()'))
            sale_num = ''.join(table0.xpath('//tr[13]/td[2]//text()'))
            area = ''.join(table0.xpath('//tr[13]/td[3]//text()'))
            table1 = html.xpath('//table')[1]
            position = ','.join(table1.xpath('.//tr[1]/td[2]//text()'))
            position = re.sub(r'\s', '', position)
            position = position[1:] if position else ''
            ca_time = re.sub(r'-', '/', ca_time)
            pan_time = ''
            price = ''
            build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
            print(build)
            Update2(build, city)
            return 1
        except requests.exceptions.ReadTimeout:
            print(url, '超时异常')
            return 1
        except Exception:
            print(url, '解析异常')
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
            company = href.split('<<<')[2]
            num = self.parse_detail(link, ca_time, company)
            if num == 1:
                time.sleep(10)
                pass
            else:
                self.db.sadd(self.redis_db, href)
def run():
    try:
        p = Producer('FjJianyang:Detail')
        p.run()
        c = Consumer('FjJianyang:Detail')
        c.run()
    except Exception as e:
        file_path=os.path.join(path,file)
        with open(file_path,'at',encoding='utf-8') as fp:
            fp.write(str(e))
            fp.write('\r')

if __name__ == '__main__':
    run()

