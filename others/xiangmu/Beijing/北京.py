# coding=utf-8
import requests
from lxml import etree
import re
import time
from common.spider_class import TongyongSpider
from common.update_mongo import Update2
import datetime
from threading import Thread
import redis
from conf.settings import REDIS_PORT, REDIS_HOST

redis_table = 'Beijing:Detail_form'
city = 'beijing'
now = datetime.datetime.now().strftime('%Y/%m/%d')
db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


class Producer(TongyongSpider):
    url = 'http://zjw.beijing.gov.cn/eportal/ui?pageId=307670'

    def get_links(self, form_data):
        for i in range(1, 10):
            try:
                response = requests.post(self.url, headers=self.headers, data=form_data, timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath(
                    '//table[@style="border-color:#BABABA;border-width:1px;border-style:Solid;font-family:宋体;width:100%;border-collapse:collapse;"]')[
                    0]
                trs = table.xpath('./tr')[1:]
                for tr in trs:
                    href = tr.xpath('./td[1]/a/@href')[0]
                    link = 'http://zjw.beijing.gov.cn' + href
                    print(link)
                    self.db.sadd(self.redis_db, link)
                return 1
            except Exception as e:
                print(form_data, e)
                if i == 9:
                    return 1

    def run(self):
        while True:
            num = self.db.scard(redis_table)
            if num == 0:
                return
            page = self.db.spop(redis_table)
            form_data = {'currentPage': '{}'.format(page)}
            self.get_links(form_data)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 10):
            try:
                response = requests.get(url, headers=self.headers, timeout=40)
                text = response.text
                html = etree.HTML(text)
                pro_name = re.sub(r'\s', '', ''.join(html.xpath('//td[@id="项目名称"]//text()')))
                company = re.sub(r'\s', '', ''.join(html.xpath('//td[@id="开发企业"]//text()')))
                ca_num = re.sub(r'\s', '', ''.join(html.xpath('//td[@id="预售许可证编号"]//text()')))
                ca_time = re.sub(r'\s', '', ''.join(html.xpath('//td[@id="发证日期"]//text()')))
                area = re.sub(r'\s', '', ''.join(html.xpath('//td[@id="准许销售面积"]//text()')))
                area = area[:-2] if area else ''
                position = re.sub(r'\s', '', ''.join(html.xpath('//td[@id="批准预售部位"]//text()')))
                span = html.xpath('//span[@id="Span1"]')
                sale_num = 0
                total_money = 0.0
                total_zoom = 0
                pan_time = ''
                if span:
                    span = span[0]
                    trs = span.xpath('.//tr')
                    for tr in trs:
                        num = re.sub(r'\s', '', ''.join(tr.xpath('./td[2]/text()')))
                        sale_num += int(num)
                        pan_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]/text()')))
                        pan_time = re.sub(r'开盘', '', pan_time)
                        price = re.sub(r'\s', '', ''.join(tr.xpath('./td[5]/text()')))
                        if price:
                            total_zoom += int(num)
                            money = float(num) * float(price)
                            total_money += money
                if sale_num == 0:
                    sale_num = ''
                    price = ''
                else:
                    if total_zoom != 0:
                        price = round(total_money / total_zoom, 2)
                        price = str(price)
                    else:
                        price = ''
                sale_num = str(sale_num)
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception as e:
                print(url, e)
                if i == 9:
                    return 1

    def run(self):
        while True:
            set_num = self.db.scard(self.redis_db)
            if set_num == 0:
                return
            link = self.db.spop(self.redis_db)
            self.parse_detail(link)


def run():
    for i in range(1, 516):
        db.sadd(redis_table, str(i))
    t_lis = []
    for i in range(1, 30):
        t = Producer('Beijing:Detail')
        pro = Thread(target=t.run)
        pro.start()
        t_lis.append(pro)
    for t in t_lis:
        t.join()
    for i in range(1, 20):
        c = Consumer('Beijing:Detail')
        pro = Thread(target=c.run)
        pro.start()


if __name__ == '__main__':
    run()
