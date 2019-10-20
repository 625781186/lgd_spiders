# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

def get_info():
    url = 'http://zrzy.jiangsu.gov.cn/gtapp/nrglIndex.action?type=2&messageID=ff8080816cd29e13016d670ff6991f29'
    response = requests.get(url, headers=headers)
    html = response.text
    print(html)
    h = etree.HTML(html)
    ls = h.xpath('/html/body/table[3]/tr/td/table[3]/tr/td')
    # print(len(ls))
    title = h.xpath('/html/body/table[3]/tr/td/table[1]/tr/td/text()')
    pat_company = re.compile(r'(.*?)：', re.S | re.M)
    pat_area = re.compile(r'出让宗地面积(.*?)土地出让年限', re.S | re.M)
    print(title)
    for i in ls:
        content = i.xpath('./p//text()')

                        # /html/body/table[3]/tbody/tr/td/table[1]/tbody/tr/td
        text = ''
        for j in content:
            text +=j
        text = text.replace('\r', '').replace('\n', '')
        company = pat_company.findall(text)
        area = pat_area.findall(text)
        # print(text)
        print(company)
        print(area)

        # content = content.replace("'\r\n\t',", "").replace("' \r\n',", "")
        # print(content)

get_info()




# def get_one():
#     url = 'http://zrzy.jiangsu.gov.cn/gtapp/nrglIndex.action?classID=2c9082b569d27630016a23ac85c61117'
#     response = requests.get(url, headers=headers)
#     html = response.text
#     # print(html)
#     h = etree.HTML(html)
#     ls = h.xpath('//td/table[@class="xxgk-listz"]/tbody/tr')
#     ls.pop(0)
#     print(len(ls))
#
#     for i in ls:
#         link = 'http://zrzy.jiangsu.gov.cn' + i.xpath('./td[2]/a/@href')[0]
#         print(link)
#         get_info(link)
# get_one()


# def get_other():
#     # for a in range(2, 5):
#     url = 'http://zrzy.jiangsu.gov.cn/gtapp/nrglIndex.action?classID=2c9082b569d27630016a23ac85c61117&type=1'
#     data = {
#         'cpage': '2'
#     }
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Cache-Control': 'max-age=0',
#         'Content-Length': '7',
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Cookie': 'JSESSIONID=871B66590473E84C58E7EA65AD001177; _gscu_769623114=6947861035lpxn43; security_session_verify=6db68524db278e2ab7f7ad5e85059672; _gscbrs_769623114=1; _gscs_769623114=69488744g2mrng43|pv:20',
#         'Host': 'zrzy.jiangsu.gov.cn',
#         'Origin': 'http://zrzy.jiangsu.gov.cn',
#         'Proxy-Connection': 'keep-alive',
#         'Referer': 'http://zrzy.jiangsu.gov.cn/gtapp/nrglIndex.action?classID=2c9082b569d27630016a23ac85c61117&type=1',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
#     }
#     response = requests.post(url, headers=headers, data=data, verify=False)
#     html = response.text
#     print(html)
#     h = etree.HTML(html)
#     ls = h.xpath('//td/table[@class="xxgk-listz"]/tbody/tr')
#     ls.pop(0)
#     print(len(ls))
#
#     for i in ls:
#         link = 'http://zrzy.jiangsu.gov.cn' + i.xpath('./td[2]/a/@href')[0]
#         print(link)
#         get_info(link)
# get_other()