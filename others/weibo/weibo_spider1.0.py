# -*- coding: utf-8 -*-
# @Time    : 2019/10/21 18:56
# @Author  : LGD
# @File    : weibo_spider1.0.py
# @功能    : 爬取微博评论


# 引入模块
import requests
import re
import csv
import codecs
import time
import json
import random
import datetime
from lxml import etree


# 请求头参数
headers = {
    'Cookie': 'SINAGLOBAL=8443581489759.424.1571220825155; un=17839931230; wvr=6; UOR=,,www.baidu.com; ULV=1571534098871:5:5:1:393573509698.06415.1571534098866:1571445789333; webim_unReadCount=%7B%22time%22%3A1571553639012%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A19%2C%22msgbox%22%3A0%7D; SCF=AjNuaLjaveFcnmRJQ893464ersNRLqbo6wJp9EsB2VglnuDkNmhZ__lI96iAsgVOZcYdDYpr_ibEswQswIuCUt0.; SUB=_2A25wqVhGDeRhGeNN71IQ-CrKyjSIHXVT386OrDV8PUNbmtANLRPDkW9NSaPYhxpdaAD_8A7TaT8vjXaoNm4fDpgk; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcdx35fr7qcMS624s398ix5JpX5KMhUgL.Fo-0Sh5p1hBceKn2dJLoIEqLxK.LBKzLBKnLxKqL1-eL1hnLxKqL1KMLBK5LxKnLB.-LBoLLMntt; SUHB=0ftpmj2viboSUb; ALF=1603165077; SSOLoginState=1571629078; Ugrow-G0=7e0e6b57abe2c2f76f677abd9a9ed65d; YF-V5-G0=bae6287b9457a76192e7de61c8d66c9d',
    'Host': 'weibo.com',
    'Referer': 'https://weibo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

class Weibo(object):
    def __init__(self) -> None:
        super().__init__()

    # 获取明星微博的id
    def get_weibo_id(self, weibo_html):

        pat_html = re.compile(r'"html":"(.*?)"}\)</script>', re.M | re.S)

        html_re = pat_html.findall(weibo_html)[0]

        pat_id_1 = re.compile(r'diss-data=\\"\\"  mid=\\"(\d{16})\\"  class=\\"WB')
        pat_id_2 = re.compile(r'diss-data=\\"\\"  mid=\\"(\d{16})\\" isForward=\\"1\\"')
        id_re_1 = pat_id_1.findall(html_re)
        id_re_2 = pat_id_2.findall(html_re)

        weibo_id_list = id_re_1 + id_re_2
        return weibo_id_list
    # 请求明星用户主页
    def get_weibo_html(self, url):
        response = requests.get(url, headers=headers, verify=False)
        return response.text


    # 构造主页url
    def make_weibo_url(self, weibo_nackname, page):
        cur_time = int(time.time() * 1000)
        url = 'https://weibo.com/{0?pids=Pl_Official_MyProfileFeed__22' \
              '&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page={1}&' \
              'ajaxpagelet=1&ajaxpagelet_v6=1&__ref=%2F{2}%3Fprofile_ftype%3D1%26page%3D2%23' \
              'feedtop&_t=FM_{3}'.format(weibo_nackname, weibo_nackname, page, cur_time)
        return url

    # 获取评论id
    def get_comment_id(self):
        pass

    # 请求获取评论页
    def get_conment_html(self):
        pass


    # 构造评论页url
    def make_comment_url(self, weibo_id, is_frist):
        if is_frist:
            url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4426895782931556&from=singleWeiBo&__rnd=1571540902627'
        else:
            url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&'
    # 启动
    def run(self):
        pass


if __name__ == '__main__':
    w = Weibo()