# -*- coding: utf-8 -*-
import pymysql
conn2 = pymysql.connect(
    user="root",
    password="",
    host="192.168.1.41",
    port=3307,
    db="lcl"
)
cur = conn2.cursor()
city_list = ['baise', 'beihai', 'dongguan', 'enshi', 'fangchenggang', 'fuzhou', 'haikou', 'huaihua', 'huanggang',
             'jian', 'jianou', 'jieyang', 'jingmen', 'jiujiang', 'liuyang', 'nanchang', 'nanchong', 'nanping',
             'neijiang', 'panzhihua', 'putian', 'qingyuan', 'ruijin', 'sanming', 'sanya', 'shenzhen', 'shiyan',
             'suining', 'test', 'tianmen', 'tongchuan', 'wuhan', 'wuyishan', 'wuzhou', 'xiaogan', 'yichang', 'yicheng',
             'yiyang', 'yueyang', 'yufu', 'zigong']
for city in city_list:
    create_table_sql = """
            CREATE TABLE %s(
                pro_name text,
                ca_num text,
                ca_time text,
                pan_time text,
                sale_num text,
                area text,
                price text,
                position text,
                company text,
                spider_time text,
                link_url text
            )engine=innodb DEFAULT CHARACTER set utf8;
             """ % city
    cur.execute(create_table_sql)
