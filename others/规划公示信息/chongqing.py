# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import pymysql
import random
import redis
from multiprocessing import Process

# REDIS_HOST = '192.168.1.77'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
# MYSQL_PASSWD = '798236031'
MYSQL_PASSWD = 'root'
MYSQL_DB = 'work_spider'

db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# conn = pymysql.connect(host='192.168.1.77', port=3306, user='root', password='798236031', db='gongchengguihua',)
# cur = conn.cursor()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

city = 'chongqing'
REDIS_URL = 'chongqing2_url'

class Chong_qing(object):
    def __init__(self):
        super().__init__()

    def get_info(self, res):
        a = 0
        while True:
            a += 1
            print(a, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            response = requests.get(res, headers=headers)
            html = response.text
            print(len(html), 'htmlhtmlhtmlhtmlhtml')
            # print(html)
            h = etree.HTML(html)
            print(len(h), 'hhhhhhhhhhhhhhhhhhhh')

            if response.status_code == 200:
                print(response.status_code)
                break
            else:
                if a == 10:
                    break

        try:
            ls = h.xpath('//*[@id="hide_div"]/table/tr/td')
            print('2333')
            print(len(ls))
            for i in ls:
                try:
                    # 规划许可证号
                    ca_num = i.xpath('//tr[1]/td[2]/text()')[0].replace(' ', '').split('\n')
                    ca_num = ''.join(ca_num)
                except:
                    ca_num = ''
                try:
                    # 发证日期
                    ca_time = i.xpath('//tr[6]/td[2]/text()')[0].replace(' ', '').split('\n')
                    ca_time = ''.join(ca_time)
                    # print(ca_time)
                except:
                    ca_time = ''

                try:
                    # 建设项目名称
                    pro_name = i.xpath('//tr[2]/td[2]/text()')[0].replace(' ', '').split('\n')
                    pro_name = ''.join(pro_name)
                except:
                    pro_name = ''
                try:
                    # 建设单位
                    jianshe_unit = i.xpath('//tr[3]/td[2]/text()')[0].replace(' ', '').split('\n')
                    jianshe_unit = ''.join(jianshe_unit)
                except:
                    jianshe_unit = ''

                # 建设位置
                pro_position = ''

                # 建设规模
                try:
                    pro_guimo = i.xpath('//tr[5]/td[2]/text()')[0].replace(' ', '').split('\n')
                    pro_guimo = ''.join(pro_guimo)
                except:
                    pro_guimo = ''

                # 所在区域
                region = ''

                # 爬取时间
                spider_time = time.strftime("%Y-%m-%d", time.localtime())

                # url
                link_url = res

                # sql = "select * from {} where ca_num=%s and ca_time=%s and pro_name=%s and jianshe_unit=%s;".format(city)
                # cur.execute(sql, [ca_num, ca_time, pro_name, jianshe_unit])
                # num = cur.fetchall()
                # if len(num) <= 0:
                #     sql = "insert into {}(id,ca_num,ca_time,pro_name,jianshe_unit,pro_position,pro_guimo,region,spider_time,link_url) VALUES (0,'%s','%s','%s','%s','%s','%s','%s','%s','%s')".format(city) % (
                #         ca_num, ca_time, pro_name, jianshe_unit, pro_position, pro_guimo, region, spider_time, link_url)
                #     print(sql)
                #     cur.execute(sql)
                #     conn.commit()

        except Exception as e:
            print(res, e)

    def get_url(self):
        for i in range(1, 1470):
            print('page-------------------------------------------------', i)
            time.sleep(random.random()*3)
            a = 0
            while True:
                a += 1
                print(a, 'aaaaaaaaaaaaa')
                url = 'http://ghzrzyj.cq.gov.cn/plus/list.php?tid=100&TotalResult=22027&PageNo={}'.format(i)
                try:
                    response = requests.get(url=url, headers=headers)
                    html = response.text
                    # print(html)
                    h = etree.HTML(html)

                    ls = h.xpath('//*[@id="100"]/li')
                    print(len(ls))
                    for i in ls:
                        # http: // ghzrzyj.cq.gov.cn / plus / view.php?aid = 150566
                        url = 'http://ghzrzyj.cq.gov.cn' + i.xpath('./a/@href')[0]
                        db.sadd(REDIS_URL, url)
                        # self.get_info(url)
                    # else:
                    #     break
                    # if response.status_code == 200:
                    #     print(response.status_code)
                    #     break

                        print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
                    print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
                except:
                    if a == 10:
                        break

    def get_run(self):
        self.get_url()


if __name__ == '__main__':
    a = Chong_qing()
    p = Process(target=a.get_run())
    p.start()
