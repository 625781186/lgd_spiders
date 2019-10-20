# -*- coding: utf-8 -*-
import requests
import random
import time
from lxml import etree
import json
import pymysql
# from gongsi_daili_ip import baidu_ip

# def get_url():
#     url = 'http://zgj.ningbo.gov.cn/col/col21811/index.html?uid=80943&pageNum=1'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
#
#     response = requests.get(url, headers=headers)
#     # print(response.apparent_encoding)
#     html = response.content.decode('utf-8')
#     print(html)
#     h = etree.HTML(html)
#     ls = h.xpath('//style/record')
#     print(len(ls))
#
# get_url()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options



# http://zgj.ningbo.gov.cn/col/col21811/index.html?uid=80943&pageNum=3
# http://zgj.ningbo.gov.cn/col/col21811/index.html?uid=80943&pageNum=3
# http://zgj.ningbo.gov.cn/col/col21811/index.html?uid=80943&pageNum=1

# chrome_options = Options()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=chrome_options)


driver = webdriver.Chrome()
driver.maximize_window()



def get_inf0(url1, time1, name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    response = requests.get(url1, headers=headers)
    html = response.content.decode('utf-8')
    # print(html)
    h = etree.HTML(html)
    jsyd = h.xpath('//*[@id="main-nr"]/text()')[3]
    if '建设用地规划许可证' in jsyd:
        # ls1 = h.xpath('//*[@id="main-nr"]/text()')
        ls2 = h.xpath('//*[@id="main-nr"]/text()')[1]
        # ls3 = h.xpath('//*[@id="main-nr"]/text()')[3]
        ls4 = h.xpath('//*[@id="main-nr"]/text()')[6]
        ls5 = h.xpath('//*[@id="main-nr"]/text()')[8]
        try:
            ca_num = ls2
        except:
            ca_num = ''

        try:
            ca_time = time1
        except:
            ca_time = ''

        try:
            pro_name = name
        except:
            pro_name = ''

        try:
            jianshe_unit = ls4
        except:
            jianshe_unit = ''

        try:
            pro_position = ls5.split('：')[1]
        except:
            pro_position = ''

        pro_guimo = ''

        region = ''

        # 爬取时间
        spider_time = time.strftime("%Y-%m-%d", time.localtime())

        # url
        link_url = url

        print(ca_num)
        print(ca_time)
        print(pro_name)
        print(jianshe_unit)
        print(pro_position)
        print(pro_guimo)
        print(region)
        print(spider_time)
        print(link_url)

        # strsql = "insert into zhejiang_ningbo(id,ca_num,ca_time,pro_name,jianshe_unit,pro_position,pro_guimo,region,spider_time,link_url) VALUES (0,'%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
        # ca_num, ca_time, pro_name, jianshe_unit, pro_position, pro_guimo, region, spider_time, link_url)
        # cur.execute(strsql)
        # conn.commit()

    else:
        pass

def get_url():
    for a in range(1, 853):
        print('page------------------------------', a)
        url = 'http://zgj.ningbo.gov.cn/col/col21811/index.html?uid=80943&pageNum={}'.format(a)
        driver.get(url)
        # input_name = driver.find_element_by_class_name('searchTitle80943').send_keys('建设')
        # btn = driver.find_element_by_class_name('crumb').click()
        try:
            ls = driver.find_elements_by_xpath('//*[@id="examineApprove1"]/li')
            ls.pop(0)
            print(len(ls))
            for i in ls:
                # http://zgj.ningbo.gov.cn/art/2019/9/5/art_21811_57155.html
                url1 = i.find_element_by_xpath('./a').get_attribute('href')
                time1 = i.find_element_by_xpath('./a/span[4]').text
                time1 = time1.split(' ')[0]
                name = i.find_element_by_xpath('./a/span[2]').text
                print(url1)
                get_inf0(url1, time1, name)
        except Exception as e:
            pass

get_url()