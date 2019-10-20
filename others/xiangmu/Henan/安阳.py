# -*- coding: utf-8 -*-
from common.spider_class import TongyongSpider
from selenium import webdriver
import requests
from lxml import etree
from selenium.webdriver.common.action_chains import ActionChains
import re
from common.update_mongo import Update
from common.update_mongo import Update2
import time
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'anyang'


class Producer(TongyongSpider):
    url = 'http://219.154.46.179:16666/Client/Nanjiang/Second/Second_HouseManger.aspx?RelationCID=2&PageSize=10'

    def __init__(self, redis_db):
        super(Producer, self).__init__(redis_db)
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        self.driver = webdriver.Chrome(options=option)
        self.redis_db = redis_db

    def get_links(self):
        self.driver.get(self.url)
        i = 0
        while True:
            time.sleep(0.5)
            source = self.driver.page_source
            html = etree.HTML(source)
            table = html.xpath('//tbody[@id="content-tbody"]')[0]
            trs = table.xpath('.//tr')
            for tr in trs:
                href = tr.xpath('./td[4]/a/@href')[0]
                company = ''.join(tr.xpath('./td[1]//text()'))
                print(company)
                link = 'http://219.154.46.179:16666/Client/Nanjiang/Second/' + href
                print(link)
                self.db.sadd(self.redis_db, link + '<<<' + company)
            next_btn = self.driver.find_element_by_xpath('//a[@id="nextPage"]/div')
            ActionChains(self.driver).move_to_element(next_btn).perform()
            next_btn.click()
            i += 1
            if i == 17:
                self.driver.close()
                return


class Consumer(TongyongSpider):
    def parse_detail(self, url, company):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code == 404: return 1
                if response.status_code == 200:
                    text = response.content.decode('utf-8')
                    html = etree.HTML(text)
                    ca_num = re.sub(r'\s', '', ''.join(html.xpath('//option[@selected="selected"]//text()')))
                    table = html.xpath('//table[@class="tableclass"]')
                    if table:
                        table = table[0]
                    else:
                        return 1
                    pro_name = re.sub(r'\s', '', ''.join(table.xpath('.//tr[1]/td[2]//text()')))
                    pan_time = re.sub(r'\s', '', ''.join(table.xpath('.//tr[8]/td[2]//text()')))
                    sale_num = re.sub(r'\s', '', ''.join(table.xpath('.//tr[9]/td[2]//text()')))
                    area = re.sub(r'\s', '', ''.join(table.xpath('.//tr[9]/td[4]//text()')))
                    price = ''
                    ca_time = ''
                    position = ''
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
            url = link.split('<<<')[0]
            company = link.split('<<<')[1]
            num = self.parse_detail(url, company)
            if num == 1:
                # time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    p = Producer('HnAnyang:Detail')
    p.get_links()
    c = Consumer('HnAnyang:Detail')
    c.run()


if __name__ == '__main__':
    run()
