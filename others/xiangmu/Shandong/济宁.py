# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import re
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')

url = 'http://www.jifcw.com/jn_web_dremis_dev/web_house_dir/crb.aspx'
city = 'jining'


class Consumer(TongyongSpider):
    url = 'http://www.jifcw.com/jn_web_dremis_dev/web_house_dir/crb.aspx'

    def get_alist(self):
        for i in range(1, 5):
            try:
                response = requests.get(self.url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                tds = html.xpath('//td[@class="SteelBlueSize"]')
                for td in tds:
                    a = td.xpath('./a/@href')[0]
                    url = 'http://www.jifcw.com/jn_web_dremis_dev/web_house_dir/' + a
                    self.db.sadd(self.redis_db, url)
            except Exception as e:
                print(e)

    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers)
                text = response.text
                html = etree.HTML(text)
                pro_name = ''.join(html.xpath('//span[@id="ctl00_ContentPlaceHolder2_lb_item_name"]//text()'))
                company = ''.join(html.xpath('//span[@id="ctl00_ContentPlaceHolder2_lb_enter_name"]//text()'))
                area = ''.join(html.xpath('//span[@id="ctl00_ContentPlaceHolder2_lb_z_area"]//text()'))
                sale_num = ''.join(html.xpath('//span[@id="ctl00_ContentPlaceHolder2_lb_z_num"]//text()'))
                trs = html.xpath(
                    '//table[@id="ctl00_ContentPlaceHolder2_Web_item_buildinfo1_GridView1"]/tr[position()>1]')
                position = []
                ca_num = ''
                for tr in trs:
                    locate = tr.xpath('./td[3]/text()')[0]
                    ca_num = tr.xpath('./td[6]/text()')[0]
                    position.append(locate)
                position = ','.join(position)
                pan_time = ''
                price = ''
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
        self.get_alist()
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
    c = Consumer('SdJining:Detail')
    c.run()


if __name__ == '__main__':
    run()
