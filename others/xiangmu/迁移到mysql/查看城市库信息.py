# -*- coding: utf-8 -*-
import pymysql
from conf.settings import MYSQL_HOST
from conf.settings import MYSQL_PORT
from conf.settings import MYSQL_PASSWD
from conf.settings import MYSQL_USER
from conf.settings import MYSQL_DB

conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
cur = conn.cursor()
dic = {
    'Beijing': ['beijing'],
    'Fujian': ['Jianyang', 'Longyan', 'Nanan', 'Quanzhou', 'Zhangzhou', 'Fuan'],
    'Guangdong': ['Guangzhou', 'Heyuan', 'Huizhou', 'Jiangmen', 'Shantou', 'Zhaoqing', 'Zhuhai'],
    'Guangxi': ['Guigang', 'Guiling', 'Nanning'],
    'Hebei': ['Cangzhou', 'Handan', 'Shijiazhuang', 'Tangshan', 'Zhangjiakou'],
    'Heilongjiang': ['Haerbin'],
    'Henan': ['Anyang', 'Kaifeng', 'Luoyang', 'Xinzheng', 'Zhengzhou', 'Zhoukou', 'Zhumadian'],
    'Liaoning': ['Anshan', 'Shenyang', 'Yingkou'],
    'Neimenggu': ['Baotou'],
    'Shandong': ['Jinan', 'Jining', 'Linyi', 'Qingdao', 'Qingzhou', 'Shouguang', 'Weihai', 'Xingtai', 'Yantai',
                 'Zaozhuang', 'Zibo'],
    'Shanxi': ['Jinzhong'],
    'Sichuan': ['Leshan', 'Luzhou'],
    'Tianjing': ['Tianjing'],
    'Yunnan': ['Kunming']
}
city_list = []
for i in dic:
    city_lis = dic[i]
    for city in city_lis:
        city_list.append(city)

# for city in city_list:
#     sql = 'select ca_num from {}'.format(city)
#     cur.execute(sql)
#     print(cur.fetchone(),city)

# 查看有多少条数据
for city in city_list:
    sql = 'select 1 from {}'.format(city)
    cur.execute(sql)
    print(len(cur.fetchall()), city)
