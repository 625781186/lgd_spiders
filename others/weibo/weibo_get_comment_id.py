# -*- coding: utf-8 -*-
# @Time    : 2019/10/21 17:00
# @Author  : LGD
# @File    : weibo_get_comment_id.py
# @功能    : 根据微博主页，获取博主的所有的微博id

import requests
import re
import csv
import codecs
import time
import json
import random
import datetime
from lxml import etree



# https://weibo.com/xiaozhan1?      pids=Pl_Official_MyProfileFeed__22  &is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=3&ajaxpagelet=1&ajaxpagelet_v6=1&__ref=%2F  xiaozhan1     %3Fis_search%3D0%26visible%3D0%26is_all%3D1%26is_tag%3D0%26profile_ftype%3D1%26page%3D2%23feedtop&_t=FM_15716477441873
# https://weibo.com/zwillingchina?  pids=Pl_Official_MyProfileFeed__23  &is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2&ajaxpagelet=1&ajaxpagelet_v6=1&__ref=%2F  zwillingchina %3F                                                        profile_ftype%3D1%26is_all%3D1%23_0&_t=FM_157163897269440
# https://weibo.com/zwillingchina?  pids=Pl_Official_MyProfileFeed__23  &is_search=0&visible=0&is_hot=1&is_tag=0&profile_ftype=1&page=2&ajaxpagelet=1&ajaxpagelet_v6=1&__ref=%2F  zwillingchina %3Fis_hot%3D1&_t=FM_157163897269428


# https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100606&is_hot=1&pagebar=1&pl_name=Pl_Official_MyProfileFeed__23&id=1006063171409662&script_uri=/zwillingchina&feed_type=0&page=1&pre_page=1&domain_op=100606&__rnd=1571653208586
headers = {
    'Cookie': 'SINAGLOBAL=8443581489759.424.1571220825155; un=17839931230; wvr=6; UOR=,,www.baidu.com; ULV=1571534098871:5:5:1:393573509698.06415.1571534098866:1571445789333; webim_unReadCount=%7B%22time%22%3A1571553639012%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A19%2C%22msgbox%22%3A0%7D; SCF=AjNuaLjaveFcnmRJQ893464ersNRLqbo6wJp9EsB2VglnuDkNmhZ__lI96iAsgVOZcYdDYpr_ibEswQswIuCUt0.; SUB=_2A25wqVhGDeRhGeNN71IQ-CrKyjSIHXVT386OrDV8PUNbmtANLRPDkW9NSaPYhxpdaAD_8A7TaT8vjXaoNm4fDpgk; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcdx35fr7qcMS624s398ix5JpX5KMhUgL.Fo-0Sh5p1hBceKn2dJLoIEqLxK.LBKzLBKnLxKqL1-eL1hnLxKqL1KMLBK5LxKnLB.-LBoLLMntt; SUHB=0ftpmj2viboSUb; ALF=1603165077; SSOLoginState=1571629078; Ugrow-G0=7e0e6b57abe2c2f76f677abd9a9ed65d; YF-V5-G0=bae6287b9457a76192e7de61c8d66c9d',
    'Host': 'weibo.com',
    'Referer': 'https://weibo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

for i in range(1, 10):
    url = 'https://weibo.com/xiaozhan1?pids=Pl_Official_MyProfileFeed__22' \
          '&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page={0}&' \
          'ajaxpagelet=1&ajaxpagelet_v6=1&__ref=%2Fxiaozhan1%3Fprofile_ftype%3D1%26page%3D2%23' \
          'feedtop&_t=FM_15716477441873'.format(i)

    response = requests.get(url, headers=headers, verify=False)
    # print(response.text)

    pat_html = re.compile(r'"html":"(.*?)"}\)</script>', re.M | re.S)

    html_re = pat_html.findall(response.text)[0]

    pat_id_1 = re.compile(r'diss-data=\\"\\"  mid=\\"(\d{16})\\"  class=\\"WB')
    pat_id_2 = re.compile(r'diss-data=\\"\\"  mid=\\"(\d{16})\\" isForward=\\"1\\"')
    id_re_1 = pat_id_1.findall(html_re)
    id_re_2 = pat_id_2.findall(html_re)

    weibo_id_list = id_re_1 + id_re_2
    print(weibo_id_list)
    time.sleep(5)
