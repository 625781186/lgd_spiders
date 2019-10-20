# -*- coding: utf-8 -*-
from lxml import etree
from common.spider_class import TongyongSpider
from common.update_mongo import Update
from common.update_mongo import Update2
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import re
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'shouguang'


class Consumer(TongyongSpider):
    def __init__(self, redis_db):
        super(Consumer, self).__init__(redis_db)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)

    def get_links(self, url):
        self.driver.get(url)
        while True:
            time.sleep(0.3)
            source = self.driver.page_source
            html = etree.HTML(source)
            table = html.xpath('//table[@class="datagrid-btable"]')[1]
            trs = table.xpath('.//tr')
            for tr in trs:
                pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[3]//text()')))
                company = re.sub(r'\s', '', ''.join(tr.xpath('./td[1]//text()')))
                position = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[5]//text()')))
                ca_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[6]//text()')))
                ca_time = re.sub(r'-', '/', ca_time)
                pan_time = ''
                price = ''
                sale_num = ''
                area = ''
                build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                print(build)
                Update2(build, city)
            next_btn = self.driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]//td[last()-3]/a')
            if 'l-btn-plain-disabled' in next_btn.get_attribute('class'):
                self.driver.close()
                return
            ActionChains(self.driver).move_to_element(next_btn).perform()
            next_btn.click()


def run():
    c = Consumer('SdShouguang:Detail')
    c.get_links('http://www.sgfcw.gov.cn/Default/YsxkList')


if __name__ == '__main__':
    run()
