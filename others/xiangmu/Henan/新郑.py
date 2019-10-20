# -*- coding: utf-8 -*-
from lxml import etree
import requests
from common.spider_class import TongyongSpider
from common.update_mongo import Update
from common.update_mongo import Update2
from selenium import webdriver
import time
import re
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city='xinzheng'


class Producer(TongyongSpider):
    def __init__(self, redis_db):
        super(Producer, self).__init__(redis_db)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)

    def get_links(self, url):
        self.driver.get(url)
        while True:
            source = self.driver.page_source
            html = etree.HTML(source)
            time.sleep(0.2)
            a_list = html.xpath('//div[@id="ctl00_ContentPlaceHolder1_houseList"]/dl/dd//a')
            for a in a_list:
                href = a.xpath('./@href')[0]
                link = 'http://www.xzsfdc.com/' + href
                pro_name = ''.join(a.xpath('.//text()'))[5:]
                print(link)
                self.db.sadd(self.redis_db, link + '<<<' + pro_name)
            next_btn = self.driver.find_element_by_xpath(
                '//a[@id="ctl00_ContentPlaceHolder1_TableNavigator1_lbtn_Next"]')
            disbaled = next_btn.get_attribute('disabled')
            if disbaled:
                self.driver.close()
                return
            next_btn.click()


class Consumer(TongyongSpider):
    def parse_detail(self, url, pro_name):
        for i in range(1,5):
            try:
                print(url)
                response = requests.get(url, headers=self.headers)
                text = response.content.decode('utf-8')
                if '数据加载失败' in text: return 1
                html = etree.HTML(text)
                table = html.xpath('//table[@id="ctl00_ContentPlaceHolder1_gv_precert"]')[0]
                ca_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[1]//text()')))
                ca_time = re.sub(r'\s', '', ''.join(table.xpath('.//tr[2]/td[3]//text()')))
                ca_time=re.sub(r'-','/',ca_time)
                price = re.sub(r'\s', '', ''.join(html.xpath('//span[@id="ctl00_ContentPlaceHolder1_lbljj"]//text()')))
                price=re.sub(r'元/㎡','',price)
                sale_num = re.sub(r'\s', '',
                                  ''.join(html.xpath('//span[@id="ctl00_ContentPlaceHolder1_lbltotalcount"]//text()')))
                company=''.join(html.xpath('//span[@id="ctl00_ContentPlaceHolder1_lbldeveloper"]//text()'))
                pan_time = ''
                area=''
                position=''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
                return 1
            except Exception as e:
                print(url,e)
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
            href = self.db.spop(self.redis_db)
            link = href.split('<<<')[0]
            pro_name = href.split('<<<')[1]
            num = self.parse_detail(link, pro_name)
            if num == 1:
                time.sleep(0.2)
                pass
            else:
                self.db.sadd(self.redis_db, href)

def run():
    p = Producer('HnXinzheng:Detail')
    p.get_links('http://www.xzsfdc.com/shangpflist.aspx')
    c = Consumer('HnXinzheng:Detail')
    c.run()


if __name__ == '__main__':
    run()
