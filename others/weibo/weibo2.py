# -*- coding: utf-8 -*-
# @Time    : 2019/10/20 10:22
# @Author  : LGD
# @File    : weibo2.py
# @功能    : 获取response.content的内容


import requests
import json
import re
import time
from lxml import etree

# url = 'https://weibo.com/aj/v6/comment/big'
url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4428454143330528&from=singleWeiBo&__rnd=1571540902627'

params = {
    'ajwvr': '6',
    'id': '4428454143330528',
    'root_comment_max_id': '4429410645860131',
    'root_comment_max_id_type': '1',
    'root_comment_ext_param': '',
    'page': '1',
    'filter': 'hot',
    'sum_comment_number': '',
    'filter_tips_before': '0',
    'from': 'singleWeiBo',
    '__rnd': '1571475170436',
}

headers = {
    # 'Cookie': 'SINAGLOBAL=8443581489759.424.1571220825155; un=17839931230; wvr=6; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; login_sid_t=255d4640b0381a7ccae639ad4264744b; cross_origin_proto=SSL; YF-V5-G0=27518b2dd3c605fe277ffc0b4f0575b3; WBStorage=384d9091c43a87a5|undefined; _s_tentry=passport.weibo.com; UOR=,,www.baidu.com; wb_view_log=1366*7681; Apache=7089734733582.643.1571280782262; ULV=1571280782275:2:2:2:7089734733582.643.1571280782262:1571220825161; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcdx35fr7qcMS624s398ix5JpX5K2hUgL.Fo-0Sh5p1hBceKn2dJLoIEqLxK.LBKzLBKnLxKqL1-eL1hnLxKqL1KMLBK5LxKnLB.-LBoLLMntt; ALF=1602816794; SSOLoginState=1571280794; SCF=AjNuaLjaveFcnmRJQ893464ersNRLqbo6wJp9EsB2VglHOgf7VgxBS8ATYlM1G3Lc3DM30oLXaeN4ggrpZD2GPA.; SUB=_2A25wo6fKDeRhGeNN71IQ-CrKyjSIHXVT2J4CrDV8PUNbmtANLU_TkW9NSaPYh455tWB1bJOKYqYKXhNQsEdsSp40; SUHB=0wn1gzGOgzMQ-Z; YF-Page-G0=b7e3c62ec2c0b957a92ff634c16e7b3f|1571280815|1571280815; wb_view_log_5340184618=1366*7681; webim_unReadCount=%7B%22time%22%3A1571280816250%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A3%2C%22msgbox%22%3A0%7D',
    'Cookie': 'SINAGLOBAL=8443581489759.424.1571220825155; un=17839931230; wvr=6; UOR=,,www.baidu.com; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; login_sid_t=dad49a60102eefe46ff826287960ebc0; cross_origin_proto=SSL; YF-V5-G0=4e19e5a0c5563f06026c6591dbc8029f; WBStorage=384d9091c43a87a5|undefined; _s_tentry=passport.weibo.com; wb_view_log=1366*7681; Apache=393573509698.06415.1571534098866; ULV=1571534098871:5:5:1:393573509698.06415.1571534098866:1571445789333; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcdx35fr7qcMS624s398ix5JpX5K2hUgL.Fo-0Sh5p1hBceKn2dJLoIEqLxK.LBKzLBKnLxKqL1-eL1hnLxKqL1KMLBK5LxKnLB.-LBoLLMntt; ALF=1603070098; SSOLoginState=1571534099; SCF=AjNuaLjaveFcnmRJQ893464ersNRLqbo6wJp9EsB2Vgl2EwqhhD8BNAEU-d3Eo65D3v_Ca72PMvklRQOAuS_GPQ.; SUB=_2A25wr8VDDeRhGeNN71IQ-CrKyjSIHXVT3LGLrDV8PUNbmtANLWaikW9NSaPYh3loQVxsscAoPQTbO42q7ALAOaE-; SUHB=0bt8ThrTWBSTRW; wb_view_log_5340184618=1366*7681; YF-Page-G0=761bd8cde5c9cef594414e10263abf81|1571534151|1571534105; webim_unReadCount=%7B%22time%22%3A1571534163749%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A17%2C%22msgbox%22%3A0%7D',
    'Host': 'weibo.com',
    'Referer': 'https://weibo.com/1797270765/Ic4eNiKzb?filter=hot&root_comment_id=0&type=comment',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

for i in range(100):
    print('========', url)
    try:
        response = requests.get(url, headers=headers, verify=False)
        html = json.loads(response.text)
        print(html)
        # html2 = json.loads(response.content)
        # print()
        html = etree.HTML(html['data']['html'])
        next_params = html.xpath('.//a[@action-type="click_more_comment"]/@action-data')
        if not next_params:
            next_params = html.xpath('.//div[@node-type="comment_loading"]/@action-data')
        # pat_url = re.compile(r'comment_loading" action-data="(.*?)&filter_tips_before=">')
        # url_params = pat_url.findall(html['data']['html'])[0]
        base_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&'
        # rnd = int(time.time() * 1000)
        # print(rnd)
        # url = base_url + next_params[0] + '&from=singleWeiBo&__rnd={0}'.format(rnd)
        url = base_url + next_params[0] + '&from=singleWeiBo&__rnd=1571540902627'
        print(url)
    except Exception as e:
        print(e)
    print(i)
    time.sleep(1)

# https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4428454143330528&root_comment_max_id=2108201649315246&root_comment_max_id_type=0&root_comment_ext_param=&page=2&filter=hot&sum_comment_number=980&filter_tips_before=0&__rnd=1571543562110
#                  /aj/v6/comment/big?ajwvr=6&id=4428454143330528&root_comment_max_id=2102429213269422&root_comment_max_id_type=0&root_comment_ext_param=&page=2&filter=hot&sum_comment_number=977&filter_tips_before=0&from=singleWeiBo&__rnd=1571543373639


