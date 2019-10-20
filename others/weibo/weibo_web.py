# -*- coding: utf-8 -*-
# @Time    : 2019/10/17 20:27
# @Author  : LGD
# @File    : weibo_web.py
# @功能    : 获取微博网页端评论信息


import requests
import re
import time
import json
import random
import datetime
from lxml import etree
from urllib.parse import parse_qs


# url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4423715674594685&root_comment_max_id=4427072308997925&root_comment_max_id_type=1&root_comment_ext_param=&page=25&filter=hot&sum_comment_number=14022&filter_tips_before=1&from=singleWeiBo&__rnd=1571316385214'
url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4428454143330528&from=singleWeiBo&__rnd=1571540902627'

# https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4428454143330528&root_comment_max_id=354480603640638&root_comment_max_id_type=0&root_comment_ext_param=&page=4&filter=hot&sum_comment_number=1110&filter_tips_before=0&from=singleWeiBo&__rnd=1571540294715
# params = {
#     'ajwvr': '6',
#     'id': '4428454143330528',
#     'root_comment_max_id': '',
#     'root_comment_max_id_type': '1',
#     'root_comment_ext_param': '',
#     'page': '1',
#     'filter': 'hot',
#     'sum_comment_number': '',
#     'filter_tips_before': '0',
#     'from': 'singleWeiBo',
#     '__rnd': '1571475170436',
# }

headers = {
    # 'Cookie': 'SINAGLOBAL=8443581489759.424.1571220825155; un=17839931230; wvr=6; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; login_sid_t=255d4640b0381a7ccae639ad4264744b; cross_origin_proto=SSL; YF-V5-G0=27518b2dd3c605fe277ffc0b4f0575b3; WBStorage=384d9091c43a87a5|undefined; _s_tentry=passport.weibo.com; UOR=,,www.baidu.com; wb_view_log=1366*7681; Apache=7089734733582.643.1571280782262; ULV=1571280782275:2:2:2:7089734733582.643.1571280782262:1571220825161; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcdx35fr7qcMS624s398ix5JpX5K2hUgL.Fo-0Sh5p1hBceKn2dJLoIEqLxK.LBKzLBKnLxKqL1-eL1hnLxKqL1KMLBK5LxKnLB.-LBoLLMntt; ALF=1602816794; SSOLoginState=1571280794; SCF=AjNuaLjaveFcnmRJQ893464ersNRLqbo6wJp9EsB2VglHOgf7VgxBS8ATYlM1G3Lc3DM30oLXaeN4ggrpZD2GPA.; SUB=_2A25wo6fKDeRhGeNN71IQ-CrKyjSIHXVT2J4CrDV8PUNbmtANLU_TkW9NSaPYh455tWB1bJOKYqYKXhNQsEdsSp40; SUHB=0wn1gzGOgzMQ-Z; YF-Page-G0=b7e3c62ec2c0b957a92ff634c16e7b3f|1571280815|1571280815; wb_view_log_5340184618=1366*7681; webim_unReadCount=%7B%22time%22%3A1571280816250%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A3%2C%22msgbox%22%3A0%7D',
    'Cookie': 'SINAGLOBAL=8443581489759.424.1571220825155; un=17839931230; wvr=6; UOR=,,www.baidu.com; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; login_sid_t=dad49a60102eefe46ff826287960ebc0; cross_origin_proto=SSL; YF-V5-G0=4e19e5a0c5563f06026c6591dbc8029f; WBStorage=384d9091c43a87a5|undefined; _s_tentry=passport.weibo.com; wb_view_log=1366*7681; Apache=393573509698.06415.1571534098866; ULV=1571534098871:5:5:1:393573509698.06415.1571534098866:1571445789333; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcdx35fr7qcMS624s398ix5JpX5K2hUgL.Fo-0Sh5p1hBceKn2dJLoIEqLxK.LBKzLBKnLxKqL1-eL1hnLxKqL1KMLBK5LxKnLB.-LBoLLMntt; ALF=1603070098; SSOLoginState=1571534099; SCF=AjNuaLjaveFcnmRJQ893464ersNRLqbo6wJp9EsB2Vgl2EwqhhD8BNAEU-d3Eo65D3v_Ca72PMvklRQOAuS_GPQ.; SUB=_2A25wr8VDDeRhGeNN71IQ-CrKyjSIHXVT3LGLrDV8PUNbmtANLWaikW9NSaPYh3loQVxsscAoPQTbO42q7ALAOaE-; SUHB=0bt8ThrTWBSTRW; wb_view_log_5340184618=1366*7681; YF-Page-G0=761bd8cde5c9cef594414e10263abf81|1571534151|1571534105; webim_unReadCount=%7B%22time%22%3A1571534163749%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A17%2C%22msgbox%22%3A0%7D',
    'Host': 'weibo.com',
    'Referer': 'https://weibo.com/1797270765/Ic4eNiKzb?filter=hot&root_comment_id=0&type=comment',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

base_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&'
# params['root_comment_max_id'] = '4426235637566576'
start = datetime.datetime.now()

for i in range(1, 10000):
    file_name = './data/weibo_fans_nickname_1000011.txt'
    try:
        # params['page'] = str(i)
        # rnd = int(time.time() * 1000)
        # print(rnd)
        # params['__rnd'] = rnd
        response = requests.get(url, headers=headers, verify=False)
        print(response.text)
        html = json.loads(response.text)['data']['html']
        html = etree.HTML(html)

        next_params = html.xpath('.//a[@action-type="click_more_comment"]/@action-data')
        if not next_params:
            next_params = html.xpath('.//div[@node-type="comment_loading"]/@action-data')

        rnd = int(time.time() * 1000)
        # print(rnd)
        url = base_url + next_params[0] + '&from=singleWeiBo&__rnd={0}'.format(rnd)
        # url = base_url + next_params[0] + '&from=singleWeiBo&__rnd=1571540902627'
        # max_id_json = html.xpath('.//div[@node-type="comment_loading"]/@action-data')
        # if not max_id_json:
        #     max_id_json = html.xpath('.//a[@action-type="click_more_comment"]/@action-data')
        # if not max_id_json:
        #     max_id_json = html.xpath('.//a[@action-type="reply"]/@action-data')

        # try:
        #     node_params = parse_qs(max_id_json[0])
        #     print(node_params)
        #     time.sleep(20)
        #     max_id = node_params['root_comment_max_id'][0]
        #
        #     number = node_params['sum_comment_number'][0]
        # except:
        #     print('cid格式==========================')
        #     node_params = parse_qs(max_id_json[0])
        #     max_id = node_params['cid'][0]
        #     number = 0
        # max_id = node_params['commentmid'][0]
        # params['root_comment_max_id'] = max_id
        # print(max_id)
        # params['root_comment_max_id'] = str(max_id)
        # params['sum_comment_number'] = str(number)

        user_list = html.xpath('.//div[@class="list_li S_line1 clearfix"]')
        print(len(user_list))
        with open(file_name, 'a', encoding='utf-8') as fw:
            for j in user_list:
                user_nickname = j.xpath('.//div[@class="WB_text"]/a[1]/text()')
                print(user_nickname)
                fw.write(user_nickname[0] + '\n')
    except Exception as e:
        print(e, datetime.datetime.date())
        if 'list index out of range' == e:
            break
    print(i)
    print('===='*30)
    time.sleep(1)
    time.sleep(random.random()*1)


cur_time = datetime.datetime.now()
print(start)
print(cur_time)




