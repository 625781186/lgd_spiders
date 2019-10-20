# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 8:40
# @Author  : LGD
# @File    : taobao.py
# @功能    : 爬取淘宝指定商品的评论，要求：100页，包含评论内容，评论日期，评论者购买的商品类别


# 引入模块
import requests
import time
import re
import json
import csv
import codecs
import random
from datetime import datetime
from lxml import etree

"""
经过分析和尝试爬取，淘宝网不需要cookies信息就可以获取数据
所以使用隧道代理提高爬取效率
"""
# 代理ip和浏览器参数设置

# 蘑菇代理的隧道订单
appKey = "Z1ZxZGZvZzVoSFI2aU1aNTo1M2xNQXZjdlRvbFBZTjV1"

# 蘑菇隧道代理服务器地址
ip_port = 'secondtransfer.moguproxy.com:9001'

# 代理协议
proxy = {"https": "https://" + ip_port}

# 请求头
headers = {
    'Proxy-Authorization': 'Basic ' + appKey,
    'cookie': 't=2f510904a1652b167e5690ddded736a2; enc=lT3GLDXH6Pa04EkYdmlDiCaP6Mt7T7p4zxSyC9NtzXVUSWJwYdjVSFGsa63XvKNLVzehDcZV8t08S%2FjnZEB8Ow%3D%3D; mt=ci=0_0; thw=cn; cookie2=161967b44afa5f1d899d4e5e7fb5d65c; _tb_token_=53e3a678eee19; cna=vny+FSuWBxsCAT2emPgYK1Ms; v=0; miid=213872151114548654; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5hmAEwUWMJdCV%2BTpmn3Ct4JuwaHGndnn098BOcf7m3jOhqgYts2WEiVJ7AytBrmjrk4DIlzg9Ing%2B5l6ZMDQcDp1Kwu5pQLTWFW1ACcbCIaXOgcQCNFdbCF53OyhQCw6sd3tYZSPD%2B2mWbkTPOHzONSAnD8tkwKgoi4UkBlS%2FwhMR6yWoz%2FrWDcR2ZEDP3pWaa%2F1CUIatD8xatnw%2FZsfaxNuIJFd1kf5WjLaPpULGX6omeWSq%2BY4ltT1i%2Ft; _m_h5_tk=a4f0fc2fe3e503a810cc1a110a3d0d50_1571492643068; _m_h5_tk_enc=7d42ed9081ba4d15ba8d08f50b4e4647; l=dBgG34Yuq6A0JznSBOfgcuI8aB_teCdf1sPzw4_g9ICPOo1c0VeRWZIaNf8kCnGVnsTXJ3RF8Ep7BfTaByUBR-ERwSlBs2JZndLh.; isg=BF9fbK0GfrxSz3qsAitdZo6Q7rMpbLPpfmhomPGpTI_FgHwC-Je1tmMSQlBbGIve',
    'Referer': 'https://item.taobao.com/item.htm?%20spm=a230r.1.14.18.783b339d98L2gF&id=598466960543&ns=1&abbucket=20',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}


# 解析数据
def analysis_data(data, file_name):
    """
    解析下载到的json文件，提取需要的字段
    :param data: json格式的数据
    :param file_name: 数据存储文件路径
    :return: 返回True表示评论不足100页，提前停止请求
    """
    data_json = json.loads(data)
    file = codecs.open(file_name, 'a', 'utf-8')
    wr = csv.writer(file)

    if data_json['comments'] == '':   # 判断评论是否少于100页，不足100页提前终止
        return True
    for j in data_json['comments']:
        comment_date = j['date']
        goods_category = j['auction']['sku'].replace('&nbsp', '').replace(';', '')
        comment_content = j['content']
        comment = [comment_date, goods_category, comment_content]
        print(comment)
        wr.writerow(comment)
    file.close()
    return False


# 下载数据
def down_url(url):
    """
    请求指定url的数据
    :param url:
    :return: 返回json格式数据
    """
    try:
        response = requests.get(url, headers=headers, proxies=proxy, verify=False)
        # 使用正则表达式提取数据
        re_str = r'jsonp_tbcrate_reviews_list\((.*?)}\)'
        pat = re.compile(re_str, re.M | re.S)
        infos_str = pat.findall(response.text)

        infos_str = infos_str[0] + '}'
        print(infos_str)
        return infos_str

    except Exception as e:    # 代理ip可能失效，本次使用的代理有效率在90%左右
        print(e)              # 代理ip失效时重新访问
        print('代理访问失败')
        down_url(url)


# 构造url
def make_url(goods_id, shop_id, page):
    """
    根据参数，构造url
    :param goods_id: 商品id
    :param shop_id: 商家id
    :param page: 页码
    :return: 返回url
    """

    # 构造时间戳，经测试天猫不需要动态时间戳，淘宝可能也不需要，暂未测试
    cur_time = time.time()
    cur_time = str(int(cur_time * 10000000) + 1000000000)
    cur_time = cur_time[:13] + '_' + cur_time[13:17]

    url = 'https://rate.taobao.com/feedRateList.htm?' \
          'auctionNumId={0}&userNumId={1}' \
          '&currentPageNum={2}&pageSize=20&orderType=sort_weight' \
          '&hasSku=false&folded=0&_ksTS={3}' \
          '&callback=jsonp_tbcrate_reviews_list'.format(goods_id, shop_id, page + 1, cur_time)
    return url


# 获取产品名称
def get_goods_name(url):
    """
    获取商品名称，用于命名
    :param url:
    :return:
    """
    while True:
        response = requests.get(url, headers=headers, proxies=proxy, verify=False)
        selector = etree.HTML(response.text)
        try:
            title = selector.xpath('//h3[@class="tb-main-title"]/text()')
        except Exception as e:
            print(e)
            title = '标题获取失败'
        if response.status_code == 200:
            break
    title = title[0].replace(' ', '').replace('\n', '').replace('\r', '')
    return title


# 主程序
if __name__ == '__main__':
    # 根据商品信息提取到的参数   ['商品id'， '商家id', '商品详情页url']
    # 此次是手动提取，可以实现自动化
    target_goods_list = [
        ['598466960543', '1610373163', 'https://item.taobao.com/item.htm?%20spm=a230r.1.14.18.783b339d98L2gF&id=598466960543&ns=1&abbucket=20#detail'],
        ['589481568715', '861584192', 'https://item.taobao.com/item.htm? spm=a230r.1.14.60.783b339d98L2gF&id=589481568715&ns=1&abbucket=20#detail'],
        ['563461287777', '240823272', 'https://item.taobao.com/item.htm? spm=a230r.1.14.124.783b339d98L2gF&id=563461287777&ns=1&abbucket=20#detail'],
        ['592244667947', '103339402', 'https://item.taobao.com/item.htm? spm=a230r.1.14.177.783b339d98L2gF&id=592244667947&ns=1&abbucket=20#detail'],
        ['592636510751', '712429244', 'https://item.taobao.com/item.htm? spm=a230r.1.14.275.783b339d98L2gF&id=592636510751&ns=1&abbucket=20#detail'],
        ['577344525909', '2074237154', 'https://item.taobao.com/item.htm? spm=a219r.lm895.14.45.32b64edcKvksqH&id=577344525909&ns=1&abbucket=20'],
        ['597577351258', '2200796501128', 'https://item.taobao.com/item.htm? spm=a219r.lm895.14.18.32b64edcKvksqH&id=597577351258&ns=1&abbucket=20'],
        ['592228899134', '2463228081', 'https://item.taobao.com/item.htm? spm=a219r.lm895.14.252.32b64edcKvksqH&id=592228899134&ns=1&abbucket=20'],
    ]
    for i in target_goods_list:

        goods_name = get_goods_name(i[2])
        date = datetime.now()
        file_name = './data_test2/{0}-{1}-{2}-{3}-淘宝.csv'.format(date.year, date.month, date.day, goods_name)

        for j in range(100):
            print('正在获取第{0}页'.format(j + 1))
            url = make_url(i[0], i[1], j)
            try:
                page_info = down_url(url)
                tag = analysis_data(page_info, file_name)
                if tag:
                    break
                time.sleep(random.random() * 2)
            except Exception as e:
                print(e)
                print('第{0}页获取失败，跳过'.format(j + 1))
                continue


