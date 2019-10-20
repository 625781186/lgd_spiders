import requests
import re
import random
import time
from lxml import etree
import json
import pymysql
# from gongsi_daili_ip import baidu_ip
from multiprocessing import Process

# conn = pymysql.connect(host='192.168.1.77', port=3306, user='root', password='798236031', db='gongchengguihua',)
# cur = conn.cursor()
city = 'zhejiang_ningbo'

# def get_ip():
#     '''
#     取ip
#     :return:
#     '''
#     proxies = baidu_ip()
#     return proxies


class Huanggang(object):
    def __init__(self):
        super().__init__()

    def get_url(self):
        for x in range(13, 17):
            print('page----------------------------------------------------', x)
            time.sleep(random.random()*2)
            # （x-1）*45+1    （x-1）*45 + 45
            # proxies = get_ip()
            try:
                url = 'http://zgj.ningbo.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={0}&endrecord={1}&perpage=15'.format((x - 1) * 45 + 1, (x - 1) * 45 + 45)

                     # http://zgj.ningbo.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=45&perpage=15
                     # http://zgj.ningbo.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=46&endrecord=90&perpage=15
                     # http://zgj.ningbo.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=91&endrecord=135&perpage=15
                     # http://zgj.ningbo.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=136&endrecord=180&perpage=15
                     # http://zgj.ningbo.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=181&endrecord=225&perpage=15

                headers = {
                    'Referer': 'http://zgj.ningbo.gov.cn/col/col21811/index.html?uid=80943&pageNum=9',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                }

                data = {
                    'col': '1',
                    'webid': '32',
                    'path': '/',
                    'columnid': '21811',
                    'sourceContentType': '1',
                    'unitid': '80943',
                    'webname': '宁波市自然资源和规划局',
                    'permissiontype': '0'
                }

                # response = requests.post(url, headers=headers, data=data, proxies=proxies)
                response = requests.post(url, headers=headers, data=data)
                # print(res.text)
                html = response.text
                # print(html)

                pat = re.compile(r'<li>(.*?)</li>', re.M | re.S)
                # pat = re.compile(r'<td align="left">(.*?)</a></td>', re.M | re.S)

                res = pat.findall(html)
                # print('----------------------------------------------------------------', res, '----------------------------------------------')
                for i in res:
                    # print(i, '======================================================================================================================================')

                    a = re.compile(r'<a class="link4 justify-end" href="(.*?)"', re.S | re.M)
                    a1 = a.findall(i)
                    a1 = ''.join(a1)
                    b = re.compile(r'')
                    print(a1, '111111111111111111111111111111111111111111111')
                    href = 'http://zgj.ningbo.gov.cn' + a1
                    print(href)

                    self.get_info(href)
            except Exception as e:
                print('page:', 1, e)

    def get_info(self, url):
        # proxies = get_ip()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        # response = requests.get(url, headers=headers, proxies=proxies)
        try:
            response = requests.get(url, headers=headers)
            html = response.content.decode('utf-8')
            # print(html)
            h = etree.HTML(html)

            jsgc = h.xpath('//*[@id="main-nr"]/text()')[3]
            # print(jsyd)
            if '建设工程规划许可证' in jsgc:
                try:
                    name1 = h.xpath('//*[@id="body1"]/div/div/div/div/div/div/h2/text()')[0]
                except:
                    name1 = ''
                try:
                    time1 = h.xpath('//*[@id="body1"]/div/div/div/div/div/div/div/span[1]/text()')[0]
                    time1 = time1.split('：')[1]
                except:
                    time1 = ''

                # ls = h.xpath('//*[@id="main-nr"]/text()')
                try:
                    ls1 = h.xpath('//*[@id="main-nr"]/text()')[1]
                except:
                    ls1 = ''
                # try:
                #     ls2 = h.xpath('//*[@id="main-nr"]/text()')[3]
                # except:
                #     ls2 = ''
                try:
                    ls3 = h.xpath('//*[@id="main-nr"]/text()')[6]
                except:
                    ls3 = ''
                try:
                    ls4 = h.xpath('//*[@id="main-nr"]/text()')[8]
                except:
                    ls4 = ''

                try:
                    ca_num = ls1
                except:
                    ca_num = ''

                try:
                    ca_time = time1
                except:
                    ca_time = ''

                try:
                    pro_name = name1
                except:
                    pro_name = ''

                try:
                    jianshe_unit = ls3
                except:
                    jianshe_unit = ''

                try:
                    pro_position = ls4.split('：')[1]
                except:
                    pro_position = ''

                pro_guimo = ''

                region = ''

                # 爬取时间
                spider_time = time.strftime("%Y-%m-%d", time.localtime())

                # url
                link_url = url

                print(ca_num)
                print(ca_time)
                print(pro_name)
                print(jianshe_unit)
                print(pro_position)
                print(pro_guimo)
                print(region)
                print(spider_time)
                print(link_url)

                # sql = "select * from {} where ca_num=%s and ca_time=%s and pro_name=%s and jianshe_unit=%s;".format(
                #     city)
                # cur.execute(sql, [ca_num, ca_time, pro_name, jianshe_unit])
                # num = cur.fetchall()
                # if len(num) <= 0:
                #     sql = "insert into {}(id,ca_num,ca_time,pro_name,jianshe_unit,pro_position,pro_guimo,region,spider_time,link_url) VALUES (0,'%s','%s','%s','%s','%s','%s','%s','%s','%s')".format(
                #         city) % (ca_num, ca_time, pro_name, jianshe_unit, pro_position, pro_guimo, region, spider_time,
                #                  link_url)
                #     print(sql)
                #     cur.execute(sql)
                #     conn.commit()

                time.sleep(random.random())

        except Exception as e:
            print(url, e)
            g = 'get_info'
            files = './{}.txt'.format(city)
            with open(files, 'a', encoding='utf-8') as file:
                file.write(e)
            file.close()
            time.sleep(random.random())

    def get_run(self):
        self.get_url()


if __name__ == '__main__':
    a = Huanggang()
    p = Process(target=a.get_run())
    p.start()