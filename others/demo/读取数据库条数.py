# -*- coding: utf-8 -*-

import pymysql

conn = pymysql.connect(host='192.168.1.77', port=3306, user="root", password="798236031", db="tyc_gongshangzhuizong")
cur = conn.cursor()
sql1 = 'show tables'
cur.execute(sql1)
datas = cur.fetchall()
a = 0
for data in datas:
    sql2 = 'select count(*) from  {}'.format(data[0])
    cur.execute(sql2)
    shu_liang = cur.fetchall()
    a += shu_liang[0][0]
print(a)
