# -*- coding: utf-8 -*-
from selenium import webdriver
from lxml import etree
import re
import time
import pymongo
import datetime
from common.update_mongo import Update2
from common.spider_class import TongyongSpider



now = datetime.datetime.now().strftime('%Y/%m/%d')
client = pymongo.MongoClient('mongodb://root:123456@127.0.0.1:27017')
city = 'heyuan'


class Producer(TongyongSpider):
    url = 'http://183.63.60.195:8608/public/web/index?jgid=FC830662-EA75-427C-9A82-443B91E383CB'

    def __init__(self, redis_db):
        super(Producer, self).__init__(redis_db)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=options)

    def get_links(self):
        self.driver.get(self.url)
        while True:
            time.sleep(1)
            source = self.driver.page_source
            html = etree.HTML(source)
            trs = html.xpath('//table[@id="listtable"]//tr')[3:]
            for tr in trs:
                href = tr.xpath('.//td[2]/a/@href')[0]
                link = 'http://183.63.60.195:8608' + href
                company = ''.join(tr.xpath('.//td[3]//text()'))
                print(link)
                self.db.sadd(self.redis_db, link + '<<<' + company)
            try:
                next_btn = self.driver.find_element_by_xpath('//a[@id="btnNext"]')
                next_btn.click()
            except Exception:
                print('全都跑完了')
                self.driver.close()
                return


class Consumer(TongyongSpider):
    def __init__(self, redis_db):
        super(Consumer, self).__init__(redis_db)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=options)

    def parse_detail(self, url, company):
        for i in range(1, 5):
            try:
                self.driver.get(url)
                time.sleep(1)
                source = self.driver.page_source
                html = etree.HTML(source)
                ca_num = ''.join(html.xpath('//font[@id="bookid"]//text()'))
                ca_num = ca_num[3:] if ca_num else ''
                pro_name = ''.join(html.xpath('//font[@id="PresellName"]//text()'))
                sale_info = re.sub(r'\s', '', ''.join(html.xpath('//font[@id="PresellArea"]//text()')))
                area = re.search(r'(.*?)平方米', sale_info)
                area = area.group(1) if area else ''
                sale_num = re.search(r'(\d+)套', sale_info)
                sale_num = sale_num.group(1) if sale_num else ''
                position = re.sub(r'\s', '', ''.join(html.xpath('//font[@id="donginfo"]//text()')))
                ca_time = ''.join(html.xpath('//font[@id="FZDate"]//text()'))
                ca_time = re.search(r'(\d+.*?日)', re.sub(r'\s', '', ca_time)).group(1) if ca_time else ''
                ca_time = re.sub(r'[年月日]', '/', ca_time)
                ca_time = ca_time[:-1] if ca_time else ''
                pan_time = ''
                price = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception:
                print(url, '解析详情异常')
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
            company = href.split('<<<')[1]
            num = self.parse_detail(link, company)
            if num == 1:
                time.sleep(2)
                pass
            else:
                self.db.sadd(self.redis_db, href)


def run():
    obj = Producer('GdHeyuan:Detail')
    obj.get_links()
    c = Consumer('GdHeyuan:Detail')
    c.run()


if __name__ == '__main__':
    run()
