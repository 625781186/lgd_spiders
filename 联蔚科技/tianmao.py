# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 11:40
# @Author  : LGD
# @File    : tianmao.py
# @功能    : 爬取天猫指定商品的评论，要求：100页，包含评论内容，评论日期，评论者购买的商品类别


# 引入模块
import requests
import time
import re
import json
import csv
import codecs
import random
from datetime import datetime


user_agent_list = [

            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",

            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",

            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",

            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",

            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",

            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",

            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",

            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",

            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",

            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",

            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",

            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",

            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",

            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",

            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",

            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",

            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",

            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",

            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"

        ]

# 请求头
headers = {
    'cookie': 'cna=vny+FSuWBxsCAT2emPgYK1Ms; lid=%E7%BA%BF%E5%AE%9D%E7%B3%96; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; enc=lT3GLDXH6Pa04EkYdmlDiCaP6Mt7T7p4zxSyC9NtzXVUSWJwYdjVSFGsa63XvKNLVzehDcZV8t08S%2FjnZEB8Ow%3D%3D; tk_trace=1; t=2f510904a1652b167e5690ddded736a2; _tb_token_=53e3a678eee19; cookie2=161967b44afa5f1d899d4e5e7fb5d65c; _m_h5_tk=116a0131b63ff469ccb408169317f24c_1571472998629; _m_h5_tk_enc=4dc07ac8c4ca8088bdccfe8542b025b3; dnk=%5Cu7EBF%5Cu5B9D%5Cu7CD6; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie15=V32FPkk%2Fw0dUvg%3D%3D&lng=zh_CN&cookie14=UoTbnKduJR7QyA%3D%3D&existShop=false&tag=8&pas=0&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C; uc3=nk2=rNXZxyRF&lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dByucmqQYwBEcDps0%3D&id2=UUplZfR9fbZ6Kw%3D%3D; tracknick=%5Cu7EBF%5Cu5B9D%5Cu7CD6; _l_g_=Ug%3D%3D; uc4=nk4=0%40rvvw8H3AM%2FDsXOdBJ9wq5pg%3D&id4=0%40U2gvKn5ZKc4v9nFwtBf%2BAl2pKvX9; unb=2244463993; lgc=%5Cu7EBF%5Cu5B9D%5Cu7CD6; cookie1=WvAz3%2B%2F06gFSlBN6ZZ7Wjm49P%2B47S3hfQjk5juF44Qk%3D; login=true; cookie17=UUplZfR9fbZ6Kw%3D%3D; _nk_=%5Cu7EBF%5Cu5B9D%5Cu7CD6; sg=%E7%B3%963e; csg=4a905254; cq=ccp%3D0; l=dBj_QFT4q6A0zalDBOCNCuI8aB_TTIRAguPRwNjDi_5Z51YsMZQOkGldbev6cjWfTwTp4B7ekLw9-etkiZnpSDbaw_aZXxDc.; isg=BDo6WM1VMx_G-L__l1Wxh8xNi2CcQ75Kgx_tq0QzuU2YN9pxLXiu1XJFh4NOpzZd',
    # 'cookie': 't=2f510904a1652b167e5690ddded736a2; _tb_token_=e36a345ed7ee9; cookie2=19cb76ee944dc714825437d871782c14; cna=vny+FSuWBxsCAT2emPgYK1Ms; dnk=%5Cu7EBF%5Cu5B9D%5Cu7CD6; lid=%E7%BA%BF%E5%AE%9D%E7%B3%96; uc4=nk4=0%40rvvw8H3AM%2FDsXOdHKjzjiNM%3D&id4=0%40U2gvKn5ZKc4v9nFwtBf%2BBFTRPtcu; csg=34248b3d; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=7205; pnm_cku822=098%23E1hvGvvUvbpvUvCkvvvvvjiPRszU1jEHRsqhAjYHPmPZ1jDPR2LZ0jEhPsMwgjYjiQhvCvvv9UUtvpvhvvvvvvGCvvpvvPMMvphvC9vhvvCvpvyCvhQUY3vvCAKxfa1l5dUf8z7OD764deQEfaBlK2kTWlK9D7zwdiB%2Bm7zvaNoAdcZI%2BExrs8TJEcqvafmxdB9aUExrsjZ7%2B3%2BIaNoxfBkKkphvC99vvOCzp8yCvv9vvUm0y01UJqyCvm9vvvvvphvvvvvv9kavpvkHvvmm86Cv2vvvvUUdphvUOQvv9krvpv3c; cq=ccp%3D1; l=dBj_QFT4q6A0zf0oBOCN5uI8aB_T8IRAguPRwNjDi_5Bl68tlX7OkgPhoFJ6cjWf9OLB4B7ekL99-etliwpTY-fP97RNTxDc.; isg=BHR0p5OjlQFjXwFNXTMX1TaDRTIm5Zi4aQHzuQ7VXP-AeRTDNl-bx0t7_fEEgdCP',
    # 'Referer': 'https://item.taobao.com/item.htm?%20spm=a230r.1.14.18.783b339d98L2gF&id=598466960543&ns=1&abbucket=20',
    'Referer': 'https://login.tmall.com/?spm=875.7931836/B.a2226mz.1.5b954265WlDcQq&redirectURL=https%3A%2F%2Fwww.tmall.com%2F%3Fspm%3Da2240.7829288.a2226n0.1.11c64fe5wemXzd',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    # 'User-Agent': user_agent_list[random.randint(1, len(user_agent_list))],
}


# 解析数据
def analysis_data(data, file_name):
    """
    解析下载到的json文件，提取需要的字段
    :param data: json格式的数据
    :param file_name: 数据存储文件路径
    :return: 返回True表示评论不足100页，提前停止请求
    """

    data_json = json.loads(data)
    file = codecs.open(file_name, 'a', 'utf-8')
    wr = csv.writer(file)
    []
    if not data_json['rateDetail']['rateList']:  # 判断评论是否存在，若评论不存在
        return True                                # 说明评论不足100页，提前停止
    for j in data_json['rateDetail']['rateList']:
        comment_date = j['rateDate']
        goods_category = j['auctionSku'].replace('&nbsp', '').replace(';', '')
        comment_content = j['rateContent']
        comment = [comment_date, goods_category, comment_content]
        print(comment)
        wr.writerow(comment)   # 逐行写入
    file.close()


# 下载数据
def down_url(url):
    """
    根据拼接的url，访问指定的评论页
    :param url:
    :return: 返回json格式的数据
    """
    try:
        response = requests.get(url, headers=headers, verify=False)
        # 使用正则表达式提取json数据
        url_pat = re.compile(r'jsonp(.*)', re.M | re.S)
        callback = url_pat.findall(url)[0]
        re_str = r'jsonp{0}\((.*?){1}\)'.format(callback, '}')
        pat = re.compile(re_str, re.M | re.S)
        infos_str = pat.findall(response.text)

        infos_str = infos_str[0] + '}'
        return infos_str

    except Exception as e:  # requests请求可能因为代理失效而失败，
        print(e)            # 判断异常防止程序终止并再次请求
        print('代理访问失败')
        down_url(url)


# 构造url
def make_url(goods_id, spu_id, seller_id, page):
    """
    拼接url
    :param goods_id: 商品id
    :param spu_id: 类别id
    :param seller_id: 商家id
    :param page: 页码
    :return: url
    """
    url = 'https://rate.tmall.com/list_detail_rate.htm?' \
          'itemId={0}&spuId={1}&sellerId={2}' \
          '&order=3&currentPage={3}&append=0&content=1' \
          '&needFold=0&_ksTS=1570880062317_1939' \
          '&callback=jsonp1940'.format(goods_id, spu_id, seller_id, page + 1)
    return url


# 获取产品名称
def get_goods_name(url):
    """
    请求商品详情页，获取商品名称，用于文件命名
    :param url:
    :return: 返回商品名称
    """

    try:
        response = requests.get(url, headers=headers, verify=False)
        pat = re.compile(r'<title>(.*?)-tmall.com天猫</title>', re.M | re.S)
        try:
            title = pat.findall(response.text)
        except Exception as e:
            print(e)
            title = '标题获取失败'
        return title[0].replace('/', '')
    except Exception as e:
        print(e)            # 防止请求失败
        get_goods_name(url)


# 主程序
if __name__ == '__main__':
    # 根据商品信息提取到的参数   ['商品id'， '类别id', '商家id', '商品详情页url']
    # 此次是手动提取，可以实现自动化

    start = datetime.now()

    target_goods_list = [
        # ['525701448082', '465322956', '92686194', 'https://detail.tmall.com/item.htm?id=525701448082'],
        # ['590662165524', '1189975479', '2167235472', 'https://detail.tmall.com/item.htm? spm=a212k0.12153887.0.0.4d29687dzOx42S&id=590662165524'],
        ['522673759226', '417159931', '2629401629', 'https://detail.tmall.com/item.htm?id=522673759226'],
        ['559267797549', '882888814', '2629401629', 'https://detail.tmall.com/item.htm?id=559267797549'],
        ['590121404469', '1185554344', '1607828329', 'https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w401118677695524.71.40e2742eDzHKEM&id=590121404469&rn=6af11002894744d4fedce93 e1f77f930&abbucket=9'],
        ['586674045789', '1147286454', '167873659', 'https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w401114900313032.102.c64838974tqWPh&id=586674045789&rn=616963fde0cc855f3d9f1d6 a1bbb59da&abbucket=9'],
        ['591214220871', '1189975479', '92686194', 'https://detail.tmall.com/item.htm?id=591214220871'],
        ['586629417046', '1148065423', '1035757927', 'https://detail.tmall.com/item.htm?id=586629417046'],
        ['536929187634', '3205331691928', '773610237', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.13873ec20QocrG&id=536929187634&skuId=3205331691928&user_id=773610237&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        ['537580775051', '3211165384820', '1047097629', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.6.13873ec20QocrG&id=537580775051&skuId=3211165384820&user_id=1047097629&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        ['540858954129', '3421779591694', '1883687207', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.11.13873ec20QocrG&id=540858954129&skuId=3421779591694&user_id=1883687207&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        ['25798100012', '3446556398539', '444076877', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.16.13873ec20QocrG&id=25798100012&skuId=3446556398539&user_id=444076877&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        ['43674527563', '3495928993765', '1903608047', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.21.13873ec20QocrG&id=43674527563&skuId=3495928993765&user_id=1903608047&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        ['585000663118', '4018274713342', '898571545', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.62.13873ec20QocrG&id=585000663118&skuId=4018274713342&user_id=898571545&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        ['599225645316', '4183246061974', '420567757', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.47.13873ec20QocrG&id=599225645316&skuId=4183246061974&user_id=420567757&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        ['556965758999', '3614910843172', '581746910', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.72.13873ec20QocrG&id=556965758999&skuId=3614910843172&user_id=581746910&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        ['4117051579530', '4117051579530', '92688455', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.56876f48oKj09D&id=584737711533&skuId=4117051579530&user_id=92688455&cat_id=2&is_b=1&rn=da514ecdcbab39703489c8b1e8853cb9'],
        ['584260512111', '3948677781377', '92688455', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.11.56876f48oKj09D&id=584260512111&skuId=3948677781377&user_id=92688455&cat_id=2&is_b=1&rn=da514ecdcbab39703489c8b1e8853cb9'],
        ['574699326330', '3763367257524', '385132127', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.23.56876f48oKj09D&id=574699326330&skuId=3763367257524&user_id=385132127&cat_id=2&is_b=1&rn=da514ecdcbab39703489c8b1e8853cb9'],
        ['569785525666', '3831238179112', '385132127', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.33.56876f48oKj09D&id=569785525666&skuId=3831238179112&user_id=385132127&cat_id=2&is_b=1&rn=da514ecdcbab39703489c8b1e8853cb9'],
        ['578803557096', '4007396314685', '2168800166', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.55.56876f48oKj09D&id=578803557096&skuId=4007396314685&user_id=2168800166&cat_id=2&is_b=1&rn=da514ecdcbab39703489c8b1e8853cb9'],
   ]
    for i in target_goods_list:
        goods_name = get_goods_name(i[3])
        date = datetime.now()
        file_name = './data_test2/{0}-{1}-{2}-{3}-天猫.csv'.format(date.year, date.month, date.day, goods_name)

        for j in range(100):
            print('正在获取第{0}页'.format(j + 1))
            url = make_url(i[0], i[1], i[2], j)
            try:
                page_info = down_url(url)
                tag = analysis_data(page_info, file_name)
                if tag:
                    break
            except Exception as e:
                print(e)
                print('第{0}页获取失败，跳过'.format(j + 1))
            # time.sleep(13)                      # 设置随机延时防止被封禁ip
            time.sleep(13)                      # 设置随机延时防止被封禁ip
            time.sleep(random.random() * 2)
            if i == 10:
                time.sleep(30)
    cur_time = datetime.now()
    print(start)
    print(cur_time)
