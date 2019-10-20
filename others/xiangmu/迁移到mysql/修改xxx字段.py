# -*- coding: utf-8 -*-
import pymysql
import re

# conn = pymysql.connect(
#     user="root",
#     password="",
#     host="192.168.1.41",
#     port=3307,
#     db="presales"
# )
conn = pymysql.connect(
    user="root",
    password="",
    host="127.0.0.1",
    port=3306,
    db="yushou2"
)
cur = conn.cursor()
sql = 'show tables;'
cur.execute(sql)
mes = cur.fetchall()

# 修改数据库时间
# for i in mes:
#     table_name = i[0]
#     if table_name == 'projcity' or table_name == 'projcity_copy':
#         continue
#     print(table_name)
#     sql = "update {} set spider_time=replace(spider_time,%s,%s)".format(table_name)
#     cur.execute(sql, ['/', '-'])
#     sql = "update {} set ca_time=replace(ca_time,%s,%s)".format(table_name)
#     cur.execute(sql, ['/', '-'])
#     sql = "update {} set pan_time=replace(pan_time,%s,%s)".format(table_name)
#     cur.execute(sql, ['/', '-'])
#     conn.commit()


# 修改XXX的值
for i in mes:
    table_name = i[0]
    print(table_name)
    if table_name == 'projcity' or table_name == 'projcity_copy':
        continue
    field_names = ['pro_name', 'ca_num', 'ca_time', 'pan_time', 'sale_num', 'area', 'price', 'position', 'company',
                   'spider_time', 'link_url']
    for field in field_names:
        sql = "update {0} set {1}=replace({1},%s,%s)".format(table_name, field)
        cur.execute(sql, ['XXX', ''])
        conn.commit()
