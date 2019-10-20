# -*- coding: utf-8 -*-
from selenium import webdriver
from lxml import etree
import requests
from selenium.webdriver.chrome.options import Options
import re
import time
from urllib import request


class LiaoChengSpider(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.url = 'http://www.lczhufang.com/servicecenter/housePresellPutInquire.html'
        self.driver = webdriver.Chrome(options=chrome_options)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def run(self):
        self.driver.get(self.url)
        time.sleep(10)
        a = self.driver.find_element_by_xpath('//div[@class="look-all"]/a')
        a.click()
        source = self.driver.page_source
        html = etree.HTML(source)
        trs = html.xpath('//tr[@class="text-c333"]')
        for tr in trs:
            pro_name = tr.xpath('./td[1]/text()')[0]
            link = tr.xpath('./td[4]/a/@href')[0]
            link = 'http://www.lczhufang.com/servicecenter' + '/' + link
            response = requests.get(url=link, headers=self.headers)
            text = response.text
            html = etree.HTML(text)
            img_links = html.xpath('//ul[@class="bigImg"]//img/@src')
            img_links = list(map(lambda x: 'http://www.lczhufang.com' + x, img_links))
            for i in range(len(img_links)):
                request.urlretrieve(img_links[i], 'images/liaocheng/' + pro_name + str(i) + '.png')


if __name__ == '__main__':
    obj = LiaoChengSpider()
    obj.run()
