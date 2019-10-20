# coding=utf-8
import requests
from lxml import etree
import re
import time
from common.spider_class import TongyongSpider
from common.update_mongo import Update2
import datetime
import os

path = os.path.dirname(__file__)
file = 'city.txt'

city = 'nanan'
now = datetime.datetime.now().strftime('%Y/%m/%d')


# 有一个网站会出异常，手动解决下
class Producer(TongyongSpider):
    url = 'http://www.nafdc.com.cn/House/link/ListPreSell?pagenumber={}&pagesize=20'

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=30)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table[@class="table tablestyles text-center"]')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    ca_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[6]//text()')))
                    ca_time = re.sub(r'-', '/', ca_time)
                    href = tr.xpath('./td[7]/a/@href')[0]
                    company = ''.join(tr.xpath('./td[3]//text()'))
                    link = 'http://www.nafdc.com.cn' + href
                    print(link)
                    self.db.sadd(self.redis_db, link + '<<<' + ca_time + '<<<' + company)
                return
            except Exception as e:
                print(url, e)
                if i == 4:
                    return

    def run(self):
        for i in range(1, 25):
            self.get_links(self.url.format(i))
            time.sleep(1)


class Consumer(TongyongSpider):
    city = 'nanan'

    def parse_detail(self, url, ca_time, company):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=30)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table[@class="table tablestyles"]')
                if table:
                    table = table[0]
                else:
                    print('没有信息')
                    return 1
                pro_name = ''.join(table.xpath('.//tr[1]/td[2]//text()'))
                ca_num = ''.join(table.xpath('.//tr[2]/td[1]//text()'))
                sale_num = ''.join(table.xpath('.//tr[13]/td[2]//text()'))
                area = ''.join(table.xpath('.//tr[13]/td[3]//text()'))
                td = html.xpath('//table[@class="tablestyles"]//td[2]')[0]
                position = ''
                a_list = td.xpath('.//a')
                for a in a_list:
                    build_num = ''.join(a.xpath('.//text()'))
                    position += ',' + build_num
                position = position[1:] if a_list else ''
                pan_time = ''
                price = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception:
                print(url, '解析详情页异常')
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
            link = href.split('<<<')[0]
            ca_time = href.split('<<<')[1]
            company = href.split('<<<')[2]
            num = self.parse_detail(link, ca_time, company)
            if num == 1:
                time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, href)


def run():
    try:
        obj = Producer('FjNanan:Detail')
        obj.run()
        c = Consumer('FjNanan:Detail')
        c.run()
    except Exception as e:
        file_path = os.path.join(path, file)
        with open(file_path, 'at', encoding='utf-8') as fp:
            fp.write(str(e))
            fp.write('\r')


if __name__ == '__main__':
    run()
