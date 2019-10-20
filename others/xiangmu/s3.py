import pymysql

connect = pymysql.connect(
    user="root",
    password="",
    host="127.0.0.1",
    port=3306,
    db="yushou2",
)
cur = connect.cursor()
sql = """
CREATE TABLE 哈尔滨(id INT PRIMARY KEY,备案名  TEXT,预售证号 TEXT,核发日期 TEXT,开盘日期 TEXT,预售套数 TEXT,预售面积'('平方米')' TEXT)
"""
dic = {
    'Beijing': ['beijing'],
    'Fujian': ['Jianyang', 'Longyan', 'Nanan', 'Quanzhou', 'Zhangzhou'],
    'Guangdong': ['Guangzhou', 'Heyuan', 'Huizhou', 'Jiangmen', 'Shantou', 'Zhaoqing', 'Zhuhai'],
    'Guangxi': ['Guigang', 'Guiling', 'Nannin'],
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
create_table_sql = '''
CREATE TABLE %s(
    id int AUTO_INCREMENT PRIMARY KEY,
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
    link_url text,
    md5 text
)engine=innodb DEFAULT CHARACTER set utf8;
 '''
for pro in dic:
    city_list = dic[pro]
    for city in city_list:
        create_table_sql = """
        CREATE TABLE %s(
            id int AUTO_INCREMENT PRIMARY KEY,
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
            link_url text,
            md5 varchar(255) unique
        )engine=innodb DEFAULT CHARACTER set utf8;
         """%city
        # data=[city]
        cur.execute(create_table_sql)
        # break
    # break
