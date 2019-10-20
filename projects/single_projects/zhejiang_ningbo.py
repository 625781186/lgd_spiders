# -*- coding: utf-8 -*-
import time
import requests
from lxml import etree
import random
import re


def get_url():
    url = 'http://zgj.ningbo.gov.cn/col/col21811/index.html?uid=80943&pageNum=1'
          # 'http://zgj.ningbo.gov.cn/col/col21811/index.html?uid=80943&pageNum=2'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    response = requests.get(url, headers=headers)
    # print(response.encoding)
    # print(response.apparent_encoding)
    html = response.content.decode('utf-8')
    pat = re.compile(r'<record>(.*?)</record>', re.S | re.M)
    pat_title = re.compile(r'title=(.*?) target="_blank">', re.S | re.M)
    pat_num = re.compile(r'<span class="single omit" style="width: 220px;">                (.*?)</span>            <span class="single omit" style="width: 250px; ">', re.S | re.M)
    pat_company = re.compile(r'<span class="single omit" style="width: 250px; ">                (.*?)</span>            <span class="single omit" style="width: 80px;text-overflow: clip; ">', re.S | re.M)
    pat_pub_time = re.compile(r'<span class="single omit" style="width: 80px;text-overflow: clip; ">                (.*?)</span>        </a>    </li>    ]]>', re.S | re.M)
    # print(html)
    ls = pat.findall(html)
    # h = etree.HTML(html)
    # ls = h.xpath('//ul[@id="examineApprove1"]/li')
    ''.split(' ')
    for i in ls:
        # print(i)
        title = pat_title.findall(i)[0]
        num = pat_num.findall(i)[0]
        company_1 = pat_company.findall(i)[0]
        company = company_1.split(' ')[-1]
        pub_time = pat_pub_time.findall(i)[0]
        print(title)
        print(num)
        # print(company_1)
        print(company)
        print(pub_time)
        print('=='*30)

get_url()