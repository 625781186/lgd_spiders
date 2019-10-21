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
    'Cookie': 'SINAGLOBAL=8443581489759.424.1571220825155; un=17839931230; wvr=6; UOR=,,www.baidu.com; ULV=1571534098871:5:5:1:393573509698.06415.1571534098866:1571445789333; webim_unReadCount=%7B%22time%22%3A1571553639012%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A19%2C%22msgbox%22%3A0%7D; SCF=AjNuaLjaveFcnmRJQ893464ersNRLqbo6wJp9EsB2VglnuDkNmhZ__lI96iAsgVOZcYdDYpr_ibEswQswIuCUt0.; SUB=_2A25wqVhGDeRhGeNN71IQ-CrKyjSIHXVT386OrDV8PUNbmtANLRPDkW9NSaPYhxpdaAD_8A7TaT8vjXaoNm4fDpgk; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcdx35fr7qcMS624s398ix5JpX5KMhUgL.Fo-0Sh5p1hBceKn2dJLoIEqLxK.LBKzLBKnLxKqL1-eL1hnLxKqL1KMLBK5LxKnLB.-LBoLLMntt; SUHB=0ftpmj2viboSUb; ALF=1603165077; SSOLoginState=1571629078; Ugrow-G0=7e0e6b57abe2c2f76f677abd9a9ed65d; YF-V5-G0=bae6287b9457a76192e7de61c8d66c9d',
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


