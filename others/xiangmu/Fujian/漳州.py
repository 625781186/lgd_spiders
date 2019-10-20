# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import time
from common.spider_class import TongyongSpider
from common.update_mongo import Update2
import datetime
from selenium import webdriver
import os

path=os.path.dirname(__file__)
file='city.txt'

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'zhangzhou'


# 有频率限制
class Producer(TongyongSpider):
    url = 'http://jsj.zhangzhou.gov.cn/cms/sitemanage/applicationIndex.shtml?applicationName=zzzjj&pageName=presellList&siteId=530418345107680000&page={}'

    def __init__(self, redis_db, cookies):
        super(Producer, self).__init__(redis_db)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.cookies = cookies

    def get_links(self, url):
        for i in range(1,5):
            try:
                response = requests.get(url, headers=self.headers, cookies=self.cookies,timeout=40)
                text = response.text
                html = etree.HTML(text)
                table = html.xpath('//table[@bgcolor]')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    href = tr.xpath('./td[3]/a/@href')[0]
                    link = 'http://jsj.zhangzhou.gov.cn' + href
                    ca_num = tr.xpath('./td[2]/text()')[0]
                    company = ''.join(tr.xpath('./td[4]//text()'))
                    ca_time = tr.xpath('./td[5]/text()')[0]
                    ca_time = re.sub(r'[年月日]', '/', ca_time)[:-1]
                    print(company)
                    self.db.sadd(self.redis_db, link + '<<<' + ca_num + '<<<' + ca_time + '<<<' + company)
                return
            except Exception as e:
                print(url, e)
                if i==4:return

    def run(self):
        urls = [self.url.format(i) for i in range(1, 219)]
        for url in urls:
            self.get_links(url)
            time.sleep(4)


class Consumer(TongyongSpider):
    def __init__(self, redis_db, cookies):
        super(Consumer, self).__init__(redis_db)
        self.redis_db = redis_db
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.cookies = cookies

    def parse_detail(self, link, ca_num, ca_time, company):
        for i in range(1,5):
            try:
                response = requests.get(link, headers=self.headers, cookies=self.cookies,timeout=40)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                table = html.xpath('//table[@bgcolor="#acacac"]')[0]
                pro_name = table.xpath('.//tr[1]/td[2]/text()')[0]
                sale_num = table.xpath('.//tr[3]/td[2]/text()')
                sale_num = sale_num[0] if sale_num else ''
                area = table.xpath('.//tr[3]/td[4]/text()')
                area = area[0] if area else ''
                table_details = html.xpath('//td[@id="dtstats"]//table')
                position = []
                total_money = 0.0
                for table_d in table_details:
                    locate = ''.join(table_d.xpath('.//tr[2]/td[1]//text()'))
                    if locate in position:
                        pass
                    else:
                        position.append(locate)
                    money = re.sub(r'\s', '', ''.join(table_d.xpath('.//tr[2]/td[8]//text()')))
                    money = float(money) if money else 0.0
                    total_money += money
                position = ','.join(position)
                if area and area != '0':
                    price = round(total_money * 10000 / float(area), 2)
                    price = str(price)
                else:
                    price = ''
                pan_time = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, link)
                print(build)
                Update2(build, city)
                return 1
            except Exception as e:
                print(link, e)
                if i==4:
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
            ca_num = link.split('<<<')[1]
            ca_time = link.split('<<<')[2]
            company = link.split('<<<')[3]
            num = self.parse_detail(url, ca_num, ca_time, company)
            if num == 1:
                time.sleep(1)
                pass
            else:
                self.db.sadd(self.redis_db, link)

def run():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(
            'http://jsj.zhangzhou.gov.cn/cms/sitemanage/applicationIndex.shtml?applicationName=zzzjj&pageName=presellList&siteId=530418345107680000&page=1')
        time.sleep(1)
        cookies = {}
        for i in driver.get_cookies():
            cookies[i['name']] = i['value']
        driver.close()
        p = Producer('FjZhangzhou:Detail', cookies)
        p.run()
        c = Consumer('FjZhangzhou:Detail', cookies)
        c.run()
    except Exception as e:
        file_path=os.path.join(path,file)
        with open(file_path,'at',encoding='utf-8') as fp:
            fp.write(str(e))
            fp.write('\r')


if __name__ == '__main__':
    run()
