# -*- coding: utf-8 -*-
from common.spider_class import TongyongSpider
import requests
from lxml import etree
import re
from common.update_mongo import Update
from common.update_mongo import Update2
import time
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'zhangjiakou'


class Producer(TongyongSpider):
    urls = ['http://www.zjk.gov.cn/%20/syscolumn/dt/tzgg/index.html'] + [
        'http://www.zjk.gov.cn/%20/syscolumn/dt/tzgg/index_1.html']

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                a_list = html.xpath('//a')
                for a in a_list:
                    content = ''.join(a.xpath('.//text()'))
                    if '申请预售许可' in content:
                        href = re.sub(r'\s', '', ''.join(a.xpath('./@href')[0]))
                        link = 'http://www.zjk.gov.cn' + href
                        print(link)
                        self.db.sadd(self.redis_db, link)
            except Exception as e:
                print(e)

    def run(self):
        for url in self.urls:
            self.get_links(url)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                table = html.xpath('//table[@style=" border:#d9d9d9 1px solid;"]')[0]
                content = re.sub(r'\s', '', ''.join(table.xpath('.//p[1]//text()')))
                pro_name = re.search(r'现就(.*?)(项目)?申请', content).group(1)
                company = re.search(r'建设单位(.*?公司)', content)
                company = company.group(1) if company else ''
                position_list = re.findall(r'\d+#', pro_name)
                position = ''
                for i in position_list:
                    position += i + '、'
                sale_info = re.sub(r'\s', '', ''.join(table.xpath('.//p[2]//text()')))
                sale_num = re.search(r'(\d+)套', sale_info)
                sale_num = sale_num.group(1) if sale_num else ''
                content = html.xpath('//td[@class="ar3"]')[1]
                content = ''.join(content.xpath('.//text()'))
                ca_time = re.search(r'(\d+年.*?)日', content).group(1)
                ca_time = re.sub(r'[年月]', '-', ca_time)
                pan_time = ''
                price = ''
                ca_num = ''
                area = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception:
                print('解析异常')
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
                # time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    p = Producer('HbZhangjiakou:Detail')
    p.run()
    c = Consumer('HbZhangjiakou:Detail')
    c.run()


if __name__ == '__main__':
    run()
