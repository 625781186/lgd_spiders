# -*- coding: utf-8 -*-
# @Time    : 2019/10/19 18:38
# @Author  : LGD
# @File    : tianmao_1.py
# @功能    :


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
cookies = ''
cookies_dict = {"_hvn_login": "0", "_tb_token_": "eba715e68e3d0", "cookie2": "1642767dfd214d4521f4d40d4be4dbbc", "csg": "9cd63383", "t": "4ff9b95584cc64fbf08d9a2b10aba5fa", "lc": "Vyu%2BvSucg0MIgCg%3D", "lid": "%E7%BA%BF%E5%AE%9D%E7%B3%96", "log": "lty=Tmc%3D", "havana_tgc": "eyJjcmVhdGVUaW1lIjoxNTcxNTMyMzk4MjQyLCJsYW5nIjoiemhfQ04iLCJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsiMCI6eyJhY2Nlc3NUeXBlIjoxLCJtZW1iZXJJZCI6MjI0NDQ2Mzk5MywidGd0SWQiOiIxbU1TdGgtUkdUVVV6V1BiTXZ3VFRsQSJ9fX19", "_cc_": "Vq8l%2BKCLiw%3D%3D", "_l_g_": "Ug%3D%3D", "_nk_": "%5Cu7EBF%5Cu5B9D%5Cu7CD6", "cookie1": "WvAz3%2B%2F06gFSlBN6ZZ7Wjm49P%2B47S3hfQjk5juF44Qk%3D", "cookie17": "UUplZfR9fbZ6Kw%3D%3D", "dnk": "%5Cu7EBF%5Cu5B9D%5Cu7CD6", "existShop": "MTU3MTUzMjM5OA%3D%3D", "lgc": "%5Cu7EBF%5Cu5B9D%5Cu7CD6", "sg": "%E7%B3%963e", "skt": "9b42a515e1003082", "tg": "0", "tracknick": "%5Cu7EBF%5Cu5B9D%5Cu7CD6", "uc1": "existShop=false&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&pas=0&cookie15=W5iHLLyFOGW7aA%3D%3D&cookie21=W5iHLLyFeYZ1WM9hVnmS&lng=zh_CN&tag=8&cookie14=UoTbnKZQZLcmTw%3D%3D", "uc3": "vt3=F8dByucnLD9gZJVdG7g%3D&nk2=rNXZxyRF&lg2=URm48syIIVrSKA%3D%3D&id2=UUplZfR9fbZ6Kw%3D%3D", "uc4": "id4=0%40U2gvKn5ZKc4v9nFwtBf%2BA8qWkWFT&nk4=0%40rvvw8H3AM%2FDsXOdA3SNzJjA%3D", "unb": "2244463993", "XSRF-TOKEN": "9082e875-5cc8-4a93-b61b-eb7b6e8c560e"}
for key, value in cookies_dict.items():
    cookies += key + '=' + value + ';'


headers = {
    # 'cookie': 'cna=vny+FSuWBxsCAT2emPgYK1Ms; '
    #           'lid=%E7%BA%BF%E5%AE%9D%E7%B3%96; '
    #           'otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; '
    #           'enc=lT3GLDXH6Pa04EkYdmlDiCaP6Mt7T7p4zxSyC9NtzXVUSWJwYdjVSFGsa63XvKNLVzehDcZV8t08S%2FjnZEB8Ow%3D%3D; '
    #           'tk_trace=1; '
    #           't=2f510904a1652b167e5690ddded736a2; '
    #           '_tb_token_=53e3a678eee19; '
    #           'cookie2=161967b44afa5f1d899d4e5e7fb5d65c; '
    #           '_m_h5_tk=116a0131b63ff469ccb408169317f24c_1571472998629; '
    #           '_m_h5_tk_enc=4dc07ac8c4ca8088bdccfe8542b025b3; '
    #           'dnk=%5Cu7EBF%5Cu5B9D%5Cu7CD6; '
    #           'uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie15=V32FPkk%2Fw0dUvg%3D%3D&lng=zh_CN&cookie14=UoTbnKduJR7QyA%3D%3D&existShop=false&tag=8&pas=0&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C; '
    #           'uc3=nk2=rNXZxyRF&lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dByucmqQYwBEcDps0%3D&id2=UUplZfR9fbZ6Kw%3D%3D; '
    #           'tracknick=%5Cu7EBF%5Cu5B9D%5Cu7CD6; _'
    #           'l_g_=Ug%3D%3D; '
    #           'uc4=nk4=0%40rvvw8H3AM%2FDsXOdBJ9wq5pg%3D&id4=0%40U2gvKn5ZKc4v9nFwtBf%2BAl2pKvX9; '
    #           'unb=2244463993; '
    #           'lgc=%5Cu7EBF%5Cu5B9D%5Cu7CD6; '
    #           'cookie1=WvAz3%2B%2F06gFSlBN6ZZ7Wjm49P%2B47S3hfQjk5juF44Qk%3D; '
    #           'login=true; '
    #           'cookie17=UUplZfR9fbZ6Kw%3D%3D; '
    #           '_nk_=%5Cu7EBF%5Cu5B9D%5Cu7CD6; '
    #           'sg=%E7%B3%963e; '
    #           'csg=4a905254; '
    #           'cq=ccp%3D0; '
    #           'l=dBj_QFT4q6A0zalDBOCNCuI8aB_TTIRAguPRwNjDi_5Z51YsMZQOkGldbev6cjWfTwTp4B7ekLw9-etkiZnpSDbaw_aZXxDc.; '
    #           'isg=BDo6WM1VMx_G-L__l1Wxh8xNi2CcQ75Kgx_tq0QzuU2YN9pxLXiu1XJFh4NOpzZd',
    'cookie': 'cna=vny+FSuWBxsCAT2emPgYK1Ms; '
              'lid=%E7%BA%BF%E5%AE%9D%E7%B3%96; '
              'otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; '
              'cq=ccp%3D1; '
              'enc=lT3GLDXH6Pa04EkYdmlDiCaP6Mt7T7p4zxSyC9NtzXVUSWJwYdjVSFGsa63XvKNLVzehDcZV8t08S%2FjnZEB8Ow%3D%3D; '
              'tk_trace=1; '
              't=2f510904a1652b167e5690ddded736a2; '
              '_tb_token_=53e3a678eee19; '
              'cookie2=161967b44afa5f1d899d4e5e7fb5d65c; '
              'dnk=%5Cu7EBF%5Cu5B9D%5Cu7CD6; '
              'uc4=nk4=0%40rvvw8H3AM%2FDsXOdBJ9wq5pg%3D&id4=0%40U2gvKn5ZKc4v9nFwtBf%2BAl2pKvX9; '
              'csg=4a905254; '
              '_m_h5_tk=a5dfc62ba3da37708bc989411a383f85_1571491071636; '
              '_m_h5_tk_enc=4f1e3d9d7fed4196babbee77dd69846b; '
              'pnm_cku822=098%23E1hvzpvUvbpvUvCkvvvvvjiPRszpgjinPLcWAjivPmP9gjrRR25Z6jnmR2qwAjl8iQhvCvvvpZptvpvhvvCvpvGCvvpvvPMMvphvC9mvphvvv8yCvv9vvhh%2BFzUEFOyCvvOCvhE2znAtvpvIvvCvpvvvvvvvvhZLvvvCKvvvBBWvvUhvvvCHhQvvv7QvvhZLvvvCfvyCvhQvIoZDjXZTKFyzOv56D46wd3gDN%2B3lHs4AnAaLINQXeB6fwhVQ0fJ6W3CQog0HKfUpejanAXZTKFyzOvxrt8TJeEtYpExreug7rj6O; '
              'l=dBj_QFT4q6A0zSZzBOCg5uI8aB_OSIRAguPRwNjDi_5BW68_x97OkGP2kFJ6cjWf9_Yp4B7ekL99-etkmppTY-fP97Rw_xDc.; '
              'isg=BMXFNMeNNO7bmxA-1CxWln_k1AE_KnmbcEaCqscqgfwLXuXQjtKJ5FM8bMINHpHM',
    # 'cookie': cookies,
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
        # ['522673759226', '417159931', '2629401629', 'https://detail.tmall.com/item.htm?id=522673759226'],
        # ['559267797549', '882888814', '2629401629', 'https://detail.tmall.com/item.htm?id=559267797549'],
        # ['590121404469', '1185554344', '1607828329', 'https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w401118677695524.71.40e2742eDzHKEM&id=590121404469&rn=6af11002894744d4fedce93 e1f77f930&abbucket=9'],
        # ['586674045789', '1147286454', '167873659', 'https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w401114900313032.102.c64838974tqWPh&id=586674045789&rn=616963fde0cc855f3d9f1d6 a1bbb59da&abbucket=9'],
        # ['591214220871', '1189975479', '92686194', 'https://detail.tmall.com/item.htm?id=591214220871'],
        # ['586629417046', '1148065423', '1035757927', 'https://detail.tmall.com/item.htm?id=586629417046'],
        # ['536929187634', '3205331691928', '773610237', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.13873ec20QocrG&id=536929187634&skuId=3205331691928&user_id=773610237&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        # ['537580775051', '3211165384820', '1047097629', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.6.13873ec20QocrG&id=537580775051&skuId=3211165384820&user_id=1047097629&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        # ['540858954129', '3421779591694', '1883687207', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.11.13873ec20QocrG&id=540858954129&skuId=3421779591694&user_id=1883687207&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        # ['25798100012', '3446556398539', '444076877', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.16.13873ec20QocrG&id=25798100012&skuId=3446556398539&user_id=444076877&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        # ['43674527563', '3495928993765', '1903608047', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.21.13873ec20QocrG&id=43674527563&skuId=3495928993765&user_id=1903608047&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        # ['585000663118', '4018274713342', '898571545', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.62.13873ec20QocrG&id=585000663118&skuId=4018274713342&user_id=898571545&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        # ['599225645316', '4183246061974', '420567757', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.47.13873ec20QocrG&id=599225645316&skuId=4183246061974&user_id=420567757&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        # ['556965758999', '3614910843172', '581746910', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.72.13873ec20QocrG&id=556965758999&skuId=3614910843172&user_id=581746910&cat_id=2&is_b=1&rn=ade8e85349239f8b0a9bac6cddf64233'],
        # ['4117051579530', '4117051579530', '92688455', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.56876f48oKj09D&id=584737711533&skuId=4117051579530&user_id=92688455&cat_id=2&is_b=1&rn=da514ecdcbab39703489c8b1e8853cb9'],
        # ['584260512111', '3948677781377', '92688455', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.11.56876f48oKj09D&id=584260512111&skuId=3948677781377&user_id=92688455&cat_id=2&is_b=1&rn=da514ecdcbab39703489c8b1e8853cb9'],
        # ['574699326330', '3763367257524', '385132127', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.23.56876f48oKj09D&id=574699326330&skuId=3763367257524&user_id=385132127&cat_id=2&is_b=1&rn=da514ecdcbab39703489c8b1e8853cb9'],
        # ['569785525666', '3831238179112', '385132127', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.33.56876f48oKj09D&id=569785525666&skuId=3831238179112&user_id=385132127&cat_id=2&is_b=1&rn=da514ecdcbab39703489c8b1e8853cb9'],
        # ['578803557096', '4007396314685', '2168800166', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.55.56876f48oKj09D&id=578803557096&skuId=4007396314685&user_id=2168800166&cat_id=2&is_b=1&rn=da514ecdcbab39703489c8b1e8853cb9'],
        ['563426935475', '3925879231735', '3570503317', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.1f92908d7X6c0L&id=563426935475&skuId=3925879231735&user_id=3570503317&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['37830376476', '48545683835', '725677994', 'https://chaoshi.detail.tmall.com/item.htm?spm=a220m.1000858.1000725.6.1f92908d7X6c0L&id=37830376476&skuId=48545683835&standard=1&user_id=725677994&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['43781780685', '77743361825', '1672097348', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.12.1f92908d7X6c0L&id=43781780685&skuId=77743361825&standard=1&user_id=1672097348&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['582320504739', '3909812029774', '3626596873', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.18.1f92908d7X6c0L&id=582320504739&skuId=3909812029774&user_id=3626596873&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['560907135330', '3905455449171', '3392536705', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.23.1f92908d7X6c0L&id=560907135330&skuId=3905455449171&user_id=3392536705&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['40217675898', '4144028176985', '1087734489', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.28.1f92908d7X6c0L&id=40217675898&skuId=4144028176985&standard=1&user_id=1087734489&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['563688699846', '3551134636378', '3570503317', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.39.1f92908d7X6c0L&id=563688699846&skuId=3551134636378&user_id=3570503317&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['563422855497', '4138911192229', '3392536705', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.44.1f92908d7X6c0L&id=563422855497&skuId=4138911192229&user_id=3392536705&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['586891579304', '4273077122670', '2200653977095', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.49.1f92908d7X6c0L&id=586891579304&skuId=4273077122670&user_id=2200653977095&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['557460543967', '4025400326836', '2790047353', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.54.1f92908d7X6c0L&id=557460543967&skuId=4025400326836&standard=1&user_id=2790047353&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['586638729188', '4156070939615', '3375170974', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.60.1f92908d7X6c0L&id=586638729188&skuId=4156070939615&user_id=3375170974&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['561837524071', '3889115270542', '3527212490', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.75.1f92908d7X6c0L&id=561837524071&skuId=3889115270542&user_id=3527212490&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['7344821848', '34529466689', '479966771', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.80.1f92908d7X6c0L&id=7344821848&skuId=34529466689&standard=1&user_id=479966771&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['595237863327', '4134517961856', '3170729146', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.105.1f92908d7X6c0L&id=595237863327&skuId=4134517961856&user_id=3170729146&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['587591880726', '4134517961856', '2200676153815', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.110.1f92908d7X6c0L&id=587591880726&skuId=4021977341140&user_id=2200676153815&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['546724870335', '4611686565152258239', '3170729146', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.119.1f92908d7X6c0L&id=546724870335&skuId=4611686565152258239&user_id=3170729146&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['42302551887', '4228835266195', '2064892827', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.128.1f92908d7X6c0L&id=42302551887&skuId=4228835266195&user_id=2064892827&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['559829737659', '4205420210000', '1773211220', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.158.1f92908d7X6c0L&id=559829737659&skuId=4205420210000&standard=1&user_id=1773211220&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['526951072980', '3872388777378', '2763096131', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.178.1f92908d7X6c0L&id=526951072980&skuId=3872388777378&user_id=2763096131&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
        ['571869973084', '4254895647051', '3375170974', 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.188.1f92908d7X6c0L&id=571869973084&skuId=4254895647051&standard=1&user_id=3375170974&cat_id=50026391&is_b=1&rn=6725808e891717b76a9be67f1bb732c0'],
  ]
    for i in target_goods_list:
        goods_name = get_goods_name(i[3])
        date = datetime.now()
        file_name = './data2/{0}-{1}-{2}-{3}-天猫.csv'.format(date.year, date.month, date.day, goods_name)

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
            time.sleep(random.random() * 1)
            # if i == 10:
            #     time.sleep(30)
    cur_time = datetime.now()
    print(start)
    print(cur_time)
