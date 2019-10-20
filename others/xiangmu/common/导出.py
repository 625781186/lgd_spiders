# -*- coding: utf-8 -*-
import pymongo
import pandas as pd

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

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
name_dic = {'beijing': '北京', 'Jianyang': '建阳', 'Longyan': '龙岩', 'Nanan': '南安', 'Quanzhou': '泉州', 'Zhangzhou': '漳州',
            'Guangzhou': '广州', 'Heyuan': '河源',
            'Huizhou': '惠州', 'Jiangmen': '江门', 'Shantou': '汕头', 'Zhaoqing': '肇庆', 'Zhuhai': '珠海', 'Guigang': '贵港',
            'Guiling': '桂林', 'Nannin': '南宁',
            'Cangzhou': '沧州', 'Handan': '邯郸', 'Shijiazhuang': '石家庄', 'Tangshan': '唐山', 'Zhangjiakou': '张家口',
            'Haerbin': '哈尔滨', 'Anyang': '安阳',
            'Kaifeng': '开封', 'Luoyang': '洛阳', 'Xinzheng': '新郑', 'Zhengzhou': '郑州', 'Zhoukou': '周口', 'Zhumadian': '驻马店',
            'Anshan': '鞍山', 'Shenyang': '沈阳',
            'Yingkou': '营口', 'Baotou': '包头', 'Jinan': '济南', 'Jining': '济宁', 'Linyi': '临沂', 'Qingdao': '青岛',
            'Qingzhou': '青州', 'Shouguang': '寿光', 'Weihai': '威海',
            'Xingtai': '邢台', 'Yantai': '烟台', 'Zaozhuang': '枣庄', 'Zibo': '淄博', 'Jinzhong': '晋中', 'Leshan': '乐山',
            'Luzhou': '泸州', 'Tianjing': '天津', 'Kunming': '昆明'
            }

from pymongo import MongoClient

client = MongoClient('mongodb://root:123456@127.0.0.1:27017')
for key in dic:
    value_list = dic[key]
    for collection in value_list:
        col = client[key][collection]
        data = list(col.find())
        df = pd.DataFrame(data)
        df.drop(['_id'], axis=1, inplace=True)
        for i in df.columns:
            df[i] = df[i].str.strip()
        name = name_dic[collection]
        print(name)
        df_new = df[
            ['备案名', '预售证号', '核发日期', '开盘日期', '预售套数', '预售面积(平方米)', '预售均价(元/平方米)', '预售部位', '项目公司', '爬取时间', '链接地址']].copy()
        df_new.to_excel(r'D:\xiangmu\data\%s.xlsx' % name, encoding='utf-8', index=False)
