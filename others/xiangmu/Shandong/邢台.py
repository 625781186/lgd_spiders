# -*- coding: utf-8 -*-
import requests
import re
import time
from lxml import etree
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'xingtai'


class Producer(TongyongSpider):
    url = 'http://zjj.xingtai.gov.cn/pplist-1562-{}.html'

    def get_links(self, url):
        response = requests.get(url, headers=self.headers,timeout=40)
        text = response.content.decode('gbk')
        html = etree.HTML(text)
        a_list = html.xpath('//div[@class="articlelist"]//li//a/@href')
        a_list = map(lambda x: 'http://zjj.xingtai.gov.cn/' + x, a_list)
        for a in a_list:
            print(a)
            self.db.sadd(self.redis_db, a)

    def run(self):
        for i in range(1, 22):
            self.get_links(self.url.format(i))
            time.sleep(1)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('gbk')
                html = etree.HTML(text)
                div = html.xpath('//div[@id="MyContent"]')[-1]
                content = re.sub(r'\s', '', ''.join(div.xpath('.//text()')))
                if '预售项目名称及楼盘号' in content:
                    pro_name = re.search(r'预售项目名称及楼盘号：?:?(.*?)房屋', content)
                    pro_name = pro_name.group(1) if pro_name else ''
                elif '项目名称' in content:
                    pro_name = re.search(r'项目名称：?:?(.*?)项目', content)
                    pro_name = pro_name.group(1) if pro_name else ''
                else:
                    pro_name = ''
                area = re.search(r'面积：?:?(\d+\.?\d+)', content)
                area = area.group(1) if area else ''
                ca_time = re.search(r'有效日期：?:?(\d+年\d+月\d+)日', content)
                ca_time = ca_time.group(1) if ca_time else ''
                ca_time = re.sub(r'[年月]', '/', ca_time)
                ca_num = re.search(r'号：?:?(.*?)号', content)
                ca_num = ca_num.group(1) + '号' if ca_num else ''
                sale_num = re.search(r'共(\d+)套', content)
                sale_num = sale_num.group(1) if sale_num else ''
                company = re.search(r'开发企业名称：?:?(.*?公司)', content)
                company = company.group(1) if company else ''
                pan_time = ''
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
            link = self.db.spop(self.redis_db)
            num = self.parse_detail(link)
            if num == 1:
                time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    p = Producer('SdXingtai:Detail')
    p.run()
    c = Consumer('SdXingtai:Detail')
    c.run()


if __name__ == '__main__':
    c = Consumer('SdXingtai:Detail')
    c.run()
