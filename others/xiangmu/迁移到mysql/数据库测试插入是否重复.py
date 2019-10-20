# -*- coding: utf-8 -*-
import pymysql


# def Update2(build, city):
#     conn = pymysql.connect(host="192.168.1.77", port=3306, user='root', passwd='798236031', db='work_spider')
#     cur = conn.cursor()
#     sql = "insert into {}(pro_name,ca_num,ca_time,pan_time,sale_num,area,price,position,company,spider_time,link_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(
#         city.lower())
#     cur.execute(sql, build)
#     conn.commit()

def Update2(build, city):
    conn = pymysql.connect(host="192.168.1.77", port=3306, user='root', passwd='798236031', db='work_spider')
    cur = conn.cursor()
    ca_num = build[1]
    company = build[8]
    pro_name = build[0]
    ca_time = build[2]
    sql = "select 1 from {} where ca_num=%s and company=%s and pro_name=%s and ca_time=%s;".format(city)
    cur.execute(sql, [ca_num, company, pro_name, ca_time])
    num = cur.fetchall()
    if len(num) > 0:
        return
    sql = "insert into {}(pro_name,ca_num,ca_time,pan_time,sale_num,area,price,position,company,spider_time,link_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(
        city.lower())
    cur.execute(sql, build)
    conn.commit()


pro_name = '水头镇海联创业园海德广场'
ca_num = '2012025'
ca_time = '2012/09/17'
pan_time = ''
sale_num = '25'
area = '5165.05'
price = ''
position = '水头镇海联创业园海德广场'
company = '福建省博德投资开发有限公司'
now = '2019/08/07'
url = 'http://www.nafdc.com.cn/House/CaseProjectInfo?CaseId=01121009014'
build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
Update2(build, 'nanan')
