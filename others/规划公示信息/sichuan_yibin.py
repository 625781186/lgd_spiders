# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import pymysql
from multiprocessing import Process
# from gongsi_daili_ip import baidu_ip


# conn = pymysql.connect(host='192.168.1.77', port=3306, user='root', password='798236031', db='gongchengguihua',)
# cur = conn.cursor()
city = 'sichuan_yibin'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
def get_ip():
    '''
    取ip
    :return:
    '''
    proxies = baidu_ip()
    return proxies


class Yibin(object):
    def __init__(self):
        super().__init__()

    def get_info(self, res):
        try:
            # proxies = get_ip()
            response = requests.get(res, headers=headers)
            html = response.content.decode('utf-8')
            # print(html)
            h = etree.HTML(html)
            ls = h.xpath('//table/tbody')
            print(len(ls))

            for j in ls:
                print('11111111111111111111111111')
                try:
                    jsdw1 = j.xpath('./tr[1]/td[1]/p/strong/span/text()')[0]
                except Exception:
                    jsdw1 = j.xpath('./tr[1]/td[1]/p/b/span/text()')[0]

                # if '建 设 单 位：' in jsdw1:
                print(jsdw1)
                ca_num = ''
                ca_time = ''
                try:
                    pro_name = j.xpath('./tr[2]/td[2]/p/span//text()')
                    pro_name = ''.join(pro_name)
                except:
                    pro_name = ''

                try:
                    # /tr[1]/td[2]/p/span
                    jianshe_unit = j.xpath('./tr[1]/td[2]/p/span/text()')[0]
                except:
                    jianshe_unit = ''

                try:
                    # 建设位置
                    # /tr[3]/td[2]/p/span
                    pro_position = j.xpath('./tr[3]/td[2]/p/span/text()')[0]
                except:
                    pro_position = ''

                # 建设规模
                try:
                    #
                    pro_guimo = j.xpath('./tr[4]/td[2]/p/span//text()')
                    pro_guimo = ''.join(pro_guimo)
                except:
                    pro_guimo = ''

                # 所在区域
                region = ''

                # 爬取时间
                spider_time = time.strftime("%Y-%m-%d", time.localtime())

                # url
                link_url = res

                print(ca_num)
                print(ca_time)
                print(pro_name)
                print(jianshe_unit)
                print(pro_position)
                print(pro_guimo)
                print(region)
                print(spider_time)
                print(link_url)
                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    # sql = "select * from {} where ca_num=%s and ca_time=%s and pro_name=%s and jianshe_unit=%s;".format(
                    #     city)
                    # cur.execute(sql, [ca_num, ca_time, pro_name, jianshe_unit])
                    # num = cur.fetchall()
                    # if len(num) <= 0:
                    #     sql = "insert into {}(id,ca_num,ca_time,pro_name,jianshe_unit,pro_position,pro_guimo,region,spider_time,link_url) VALUES (0,'%s','%s','%s','%s','%s','%s','%s','%s','%s')".format(
                    #         city) % (
                    #               ca_num, ca_time, pro_name, jianshe_unit, pro_position, pro_guimo, region,
                    #               spider_time,
                    #               link_url)
                    #     print(sql)
                    #     cur.execute(sql)
                    #     conn.commit()

                # else:
                    #                 /tr[1]/td[1]/p/b/span
                    # print('222222222222222')
                    # jsdw2 = j.xpath('./tr[1]/td[1]/p/b/span/text()')[0]
                    # print(jsdw2)
                    # if '建 设 单 位：' in jsdw2:
                    #     ca_num = ''
                    #     ca_time = ''
                    #     try:
                    #         #                    /tr[2]/td[2]/p/span[1]
                    #         pro_name = j.xpath('./tr[2]/td[2]/p/span//text()')
                    #         pro_name = ''.join(pro_name)
                    #     except:
                    #         pro_name = ''
                    #
                    #     try:
                    #                                # /tr[1]/td[2]/p/span
                    #                 # //*[@id="eWebEditor_Excel_Sheet_Div1"]/table/tbody/tr[1]/td[2]/p/span
                    #         jianshe_unit = j.xpath('./tr[1]/td[2]/p/span/text()')
                    #         jianshe_unit = ''.join(jianshe_unit)
                    #     except:
                    #         jianshe_unit = ''
                    #
                    #     try:
                    #         # 建设位置
                    #         # /tr[3]/td[2]/p
                    #         pro_position = j.xpath('./tr[3]/td[2]/p/span//text()')
                    #         pro_position = ''.join(pro_position)
                    #     except:
                    #         pro_position = ''
                    #
                    #     # 建设规模
                    #     try:
                    #         # /tr[4]/td[2]/p/span
                    #         pro_guimo = j.xpath('./tr[4]/td[2]/p/span//text()')
                    #         pro_guimo = ''.join(pro_guimo)
                    #     except:
                    #         pro_guimo = ''
                    #
                    #     # 所在区域
                    #     region = ''
                    #
                    #     # 爬取时间
                    #     spider_time = time.strftime("%Y-%m-%d", time.localtime())
                    #
                    #     # url
                    #     link_url = res

                        # print(ca_num)
                        # print(ca_time)
                        # print(pro_name)
                        # print(jianshe_unit)
                        # print(pro_position)
                        # print(pro_guimo)
                        # print(region)
                        # print(spider_time)
                        # print(link_url)
                        # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

                        # sql = "select * from {} where ca_num=%s and ca_time=%s and pro_name=%s and jianshe_unit=%s;".format(
                        #     city)
                        # cur.execute(sql, [ca_num, ca_time, pro_name, jianshe_unit])
                        # num = cur.fetchall()
                        # if len(num) <= 0:
                        #     sql = "insert into {}(id,ca_num,ca_time,pro_name,jianshe_unit,pro_position,pro_guimo,region,spider_time,link_url) VALUES (0,'%s','%s','%s','%s','%s','%s','%s','%s','%s')".format(
                        #         city) % (
                        #               ca_num, ca_time, pro_name, jianshe_unit, pro_position, pro_guimo, region,
                        #               spider_time,
                        #               link_url)
                        #     print(sql)
                        #     cur.execute(sql)
                        #     conn.commit()

                    # else:
                    #     slrq3 = j.xpath('./tr[1]/td[1]/p/font/text()')[0]
                    #     if '受理日期' in slrq3:
                    #         ca_num = ''
                    #         ca_time = ''
                    #         try:
                    #             # /tr[4]/td[2]/p/font
                    #             pro_name = j.xpath('./tr[4]/td[2]/p/font/text()')
                    #             pro_name = ''.join(pro_name)
                    #         except:
                    #             pro_name = ''
                    #
                    #         try:
                    #             # ./tr[3]/td[2]/font
                    #             jianshe_unit = j.xpath('./tr[3]/td[2]/font/text()')
                    #             jianshe_unit = ''.join(jianshe_unit)
                    #         except:
                    #             jianshe_unit = ''
                    #
                    #         try:
                    #             # 建设位置
                    #             # /tr[6]/td[2]/font
                    #             pro_position = j.xpath('./tr[6]/td[2]/font/text()')
                    #             pro_position = ''.join(pro_position)
                    #         except:
                    #             pro_position = ''
                    #
                    #         # 建设规模
                    #         try:
                    #             # /tr[7]/td[2]/p/font
                    #             pro_guimo = j.xpath('./tr[7]/td[2]/p/font/text()')
                    #             pro_guimo = ''.join(pro_guimo)
                    #         except:
                    #             pro_guimo = ''
                    #
                    #         # 所在区域
                    #         region = ''
                    #
                    #         # 爬取时间
                    #         spider_time = time.strftime("%Y-%m-%d", time.localtime())
                    #
                    #         # url
                    #         link_url = res
                    #
                    #
                    #         print(ca_num)
                    #         print(ca_time)
                    #         print(pro_name)
                    #         print(jianshe_unit)
                    #         print(pro_position)
                    #         print(pro_guimo)
                    #         print(region)
                    #         print(spider_time)
                    #         print(link_url)
                    #         print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

                            # sql = "select * from {} where ca_num=%s and ca_time=%s and pro_name=%s and jianshe_unit=%s;".format(
                            #     city)
                            # cur.execute(sql, [ca_num, ca_time, pro_name, jianshe_unit])
                            # num = cur.fetchall()
                            # if len(num) <= 0:
                            #     sql = "insert into {}(id,ca_num,ca_time,pro_name,jianshe_unit,pro_position,pro_guimo,region,spider_time,link_url) VALUES (0,'%s','%s','%s','%s','%s','%s','%s','%s','%s')".format(
                            #         city) % (
                            #               ca_num, ca_time, pro_name, jianshe_unit, pro_position, pro_guimo, region,
                            #               spider_time,
                            #               link_url)
                            #     print(sql)
                            #     cur.execute(sql)
                            #     conn.commit()
                        # else:
                        #     pass
        except Exception as e:
            print(res, e)

    def get_url(self):
        for a in range(3):
            if a == 0:
                url = 'http://zygh.yibin.gov.cn/yssz/jsgcghxkz/index.html'
            else:
                url = 'http://zygh.yibin.gov.cn/yssz/jsgcghxkz/index_{}.html'.format(a)
            # proxies = get_ip()
            # response = requests.get(url=url, headers=headers, proxies=proxies)
            response = requests.get(url=url, headers=headers)
            html = response.content.decode('utf-8')
            # print(html)
            h = etree.HTML(html)
            ls = h.xpath('/html/body/div[8]/div[1]/div[2]/div[2]/div[1]/ul/li')
            print(len(ls))
            for i in ls:
                     # http://zygh.yibin.gov.cn/yssz/jsgcghxkz/201802/t20180214_924566.html
                url = 'http://zygh.yibin.gov.cn/yssz/jsgcghxkz' + i.xpath('./a/@href')[0].split('.', 1)[1]
                self.get_info(url)

    def get_num(self):
        for a in range(3):
            pass


if __name__ == '__main__':
    a = Yibin()
    p = Process(target=a.get_url())
    p.start()