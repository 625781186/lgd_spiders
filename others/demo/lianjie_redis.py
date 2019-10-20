# -*- coding: utf-8 -*-
# @Time    : 2019/10/20 14:28
# @Author  : LGD
# @File    : lianjie_redis.py
# @功能    :


import requests
import json
import redis
import pymysql
# import xlrd, re
from lxml import etree
from multiprocessing import Process, Lock, Pool, Pipe
import re
from time import sleep
from fake_useragent import UserAgent
ua=UserAgent()
bbb=ua.random
db0 = redis.StrictRedis(host='192.168.1.140', port=6379, decode_responses=True, db=0)
db3 = redis.StrictRedis(host='192.168.1.139', port=6379, decode_responses=True, db=3)
conn = pymysql.connect(host='192.168.1.139', port=3306, user="root", password="root", db="数据变动")
cur = conn.cursor()

# 保存
def pipeline(company,biangengntime, fengxianjibie, biangengleixing, binagengneirong):
    print(biangengntime, fengxianjibie, biangengleixing, binagengneirong)
    print('正在写入 ')
    sql = 'insert into 50w公司变更 values (%s,%s,%s,%s,%s)'
    parmars = [company, biangengntime, fengxianjibie, biangengleixing, binagengneirong]
    print(parmars)
    cur.execute(sql, parmars)
    conn.commit()
    print('success')


def get_ip():
    '''
    取ip
    :return:
    '''
    while True:
        try:
            ips = db0.smembers('LandPool')
            # print(ips)
            for ip in ips:
                proxy = {
                    'http': '%s' % ip,
                    'https': '%s' % ip
                }
                db0.srem('LandPool', ip)
                aaa = requests.get('https://www.baidu.com/', proxies=proxy, timeout=2)
                # print(aaa.status_code)
                if aaa.status_code == 200:
                    return proxy
                else:
                    pass
        except:
            pass


def jiexie(table, x, company):
    biangengntime = table.xpath('.//tr['+str(x)+']/td[1]//text()')
    biangengntime = "".join(biangengntime)
    biangengntime = "".join(biangengntime.split())
    fengxianjibie = table.xpath('.//tr['+str(x)+']/td[2]//text()')
    fengxianjibie = "".join(fengxianjibie)
    fengxianjibie = "".join(fengxianjibie.split())
    biangengleixing = table.xpath('.//tr['+str(x)+']/td[3]//text()')
    biangengleixing = "".join(biangengleixing)
    biangengleixing = "".join(biangengleixing.split())
    binagengneirong = table.xpath('.//tr['+str(x)+']/td[4]//text()')
    binagengneirong = "".join(binagengneirong)
    binagengneirong = "".join(binagengneirong.split())
    return company,biangengntime, fengxianjibie, biangengleixing, binagengneirong


def getqiyedongtai(unique, cookies, i, company):
    proxies = get_ip()
    print(proxies, '*'*50, company, unique)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': cookies,
        'Host': 'www.qichacha.com',
        'Referer': 'https://www.qichacha.com/firm_'+unique+'.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': bbb,
        }
    parmar = {
        'keyno': unique,
        'companyname': company
    }
    # res = session.get('https://www.qichacha.com/', proxies=proxies, headers=headers, timeout=5)
    # cookies = requests.utils.dict_from_cookiejar(res.cookies)
    url = 'https://www.qichacha.com/company_intelligence?keyno='+unique+'&p='+str(i)
    print(url)
    res1 = requests.get(url, proxies=proxies, headers=headers, params=parmar,timeout=5)
    html = res1.text
    select = etree.HTML(html)
    # print(html)
    # print(len(html))
    try:
        table = select.xpath('/html/body/div[1]/div/div[2]')[0]
        long = table.xpath('.//tr')
        # print(long,'long')
        for x in range(len(long)):
            if x == 0:
                pass
            else:
                # x=x+1
                # print(x)
                company1, biangengntime, fengxianjibie, biangengleixing, binagengneirong=jiexie(table, x, company)
                pipeline(company, biangengntime, fengxianjibie, biangengleixing, binagengneirong)
        if len(long) > 20:
            getqiyedongtai(unique, cookies=cookies, i=i+1, company=company)
        else:
            # print('99，len(long) < 20:')
            return
    except Exception as e:
        db3.sadd(company, unique)
        print(e, '保存库里换个ip', 117)


def main():
    while True:
        keys = db3.keys()
        if not keys:
            # keys等于空列表的时候 执行break
            break
        else:
            for company in keys:
                unique = str(db3.spop(company))
                if unique == 'None':
                    pass
                else:
                    cookies = 'QCCSESSID=fb09v9562k14dt94r0dsnsqhf7; UM_distinctid=16dd985092e23a-0f478036a95bb7-5c40291e-1fa400-16dd985092f6ff; CNZZDATA1254842228=1378154342-1571309516-https%253A%252F%252Fsp0.baidu.com%252F%7C1571309516; zg_did=%7B%22did%22%3A%20%2216dd985097b8b3-05e908a0f8b5c2-5c40291e-1fa400-16dd985097c996%22%7D; hasShow=1; _uab_collina=157131243776961349485533; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1571312438; acw_tc=3a31f82215713124372658022e7a17c4d7a5ffeb39cdecc1f9bc440521; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1571312525; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201571312437631%2C%22updated%22%3A%201571312530966%2C%22info%22%3A%201571312437636%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22sp0.baidu.com%22%2C%22cuid%22%3A%20%2251d66881582329f189af5c630d3a10c4%22%7D'
                    try:
                        getqiyedongtai(unique, i=1, cookies=cookies, company=company)
                    except:
                        db3.sadd(company, unique)


if __name__ == '__main__':
    main()