# -*- coding: utf-8 -*-
# @Time    : 2019/10/17 20:27
# @Author  : LGD
# @File    : weibo_web.py
# @功能    : 获取微博网页端评论信息


import requests
import re
import csv
import codecs
import time
import json
import random
import datetime
from lxml import etree
from urllib.parse import parse_qs


# url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4423715674594685&root_comment_max_id=4427072308997925&root_comment_max_id_type=1&root_comment_ext_param=&page=25&filter=hot&sum_comment_number=14022&filter_tips_before=1&from=singleWeiBo&__rnd=1571316385214'
url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4426895782931556&from=singleWeiBo&__rnd=1571540902627'


headers = {
    'Cookie': 'SINAGLOBAL=8443581489759.424.1571220825155; un=17839931230; wvr=6; UOR=,,www.baidu.com; ULV=1571534098871:5:5:1:393573509698.06415.1571534098866:1571445789333; webim_unReadCount=%7B%22time%22%3A1571553639012%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A19%2C%22msgbox%22%3A0%7D; SCF=AjNuaLjaveFcnmRJQ893464ersNRLqbo6wJp9EsB2VglnuDkNmhZ__lI96iAsgVOZcYdDYpr_ibEswQswIuCUt0.; SUB=_2A25wqVhGDeRhGeNN71IQ-CrKyjSIHXVT386OrDV8PUNbmtANLRPDkW9NSaPYhxpdaAD_8A7TaT8vjXaoNm4fDpgk; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcdx35fr7qcMS624s398ix5JpX5KMhUgL.Fo-0Sh5p1hBceKn2dJLoIEqLxK.LBKzLBKnLxKqL1-eL1hnLxKqL1KMLBK5LxKnLB.-LBoLLMntt; SUHB=0ftpmj2viboSUb; ALF=1603165077; SSOLoginState=1571629078; Ugrow-G0=7e0e6b57abe2c2f76f677abd9a9ed65d; YF-V5-G0=bae6287b9457a76192e7de61c8d66c9d',
    'Host': 'weibo.com',
    'Referer': 'https://weibo.com/1797270765/Ic4eNiKzb?filter=hot&root_comment_id=0&type=comment',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

base_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&'
file_name = './data/weibo_id_肖战.txt'


for i in range(1, 8000):
    try:
        id_set = set()
        response = requests.get(url, headers=headers, verify=False)
        # print(response.text)
        html = json.loads(response.text)['data']['html']
        html = etree.HTML(html)

        next_params = html.xpath('.//a[@action-type="click_more_comment"]/@action-data')
        if not next_params:
            next_params = html.xpath('.//div[@node-type="comment_loading"]/@action-data')

        rnd = int(time.time() * 1000)
        url = base_url + next_params[0] + '&from=singleWeiBo&__rnd={0}'.format(rnd)

        user_list = html.xpath('.//div[@class="list_li S_line1 clearfix"]')
        print(len(user_list))
        # with open(file_name, 'a', encoding='utf-8') as fw:

        for j in user_list:
            userid = j.xpath('.//div[@class="WB_text"]/a[1]/@usercard')
            print(userid)
            id_set.add(userid[0].replace('id=', ''))
        id_list = list(id_set)
        with open(file_name, 'a', encoding='utf-8') as wr:
            for k in id_list:
                wr.write(k + '\n')

    except Exception as e:
        print(e)
        if 'list index out of range' == e:
            break

    print(i)
    print('===='*30)
    # time.sleep(1)
    time.sleep(random.random()*1)

# cur_time = datetime.datetime.now()
# print(start)
# print(cur_time)




