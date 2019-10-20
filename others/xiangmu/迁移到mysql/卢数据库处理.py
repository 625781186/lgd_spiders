# -*- coding: utf-8 -*-
import pymysql

conn = pymysql.connect(
    user="root",
    password="123456",
    host="127.0.0.1",
    port=3306,
    db="规范数据库"
)
conn2 = pymysql.connect(
    user="root",
    password="",
    host="192.168.1.41",
    port=3307,
    db="lcl"
)
cur = conn.cursor()
cur2 = conn2.cursor()
city_list = ['baise', 'beihai', 'dongguan', 'enshi', 'fangchenggang', 'fuzhou', 'haikou', 'huaihua', 'huanggang',
             'jian', 'jianou', 'jieyang', 'jingmen', 'jiujiang', 'liuyang', 'nanchang', 'nanchong', 'nanping',
             'neijiang', 'panzhihua', 'putian', 'qingyuan', 'ruijin', 'sanming', 'sanya', 'shenzhen', 'shiyan',
             'suining', 'test', 'tianmen', 'tongchuan', 'wuhan', 'wuyishan', 'wuzhou', 'xiaogan', 'yichang', 'yicheng',
             'yiyang', 'yueyang', 'yufu', 'zigong']
for city in city_list:
    sql = 'select * from %s' % city
    cur.execute(sql)
    mes = cur.fetchall()
    data = list(mes)
    sql = "insert into {}(pro_name,ca_num,ca_time,pan_time,sale_num,area,price,position,company,spider_time,link_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(
        city.lower())
    cur2.executemany(sql, data)
    conn2.commit()
