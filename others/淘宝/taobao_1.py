# -*- coding: utf-8 -*-
# @Time    : 2019/10/19 19:02
# @Author  : LGD
# @File    : taobao_1.py
# @功能    :


import requests
import time

# 蘑菇代理的隧道订单
appKey = "Z1ZxZGZvZzVoSFI2aU1aNTo1M2xNQXZjdlRvbFBZTjV1"

# 蘑菇隧道代理服务器地址
ip_port = 'secondtransfer.moguproxy.com:9001'

# 代理协议
proxy = {"https": "https://" + ip_port}

# url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=573438501591&userNumId=2242712302&currentPageNum=4&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&_ksTS=1571483526605_1843&callback=jsonp_tbcrate_reviews_list'
cookies = ''
cookies_dict = {"_hvn_login": "0", "_tb_token_": "eba715e68e3d0", "cookie2": "1642767dfd214d4521f4d40d4be4dbbc", "csg": "9cd63383", "t": "4ff9b95584cc64fbf08d9a2b10aba5fa", "lc": "Vyu%2BvSucg0MIgCg%3D", "lid": "%E7%BA%BF%E5%AE%9D%E7%B3%96", "log": "lty=Tmc%3D", "havana_tgc": "eyJjcmVhdGVUaW1lIjoxNTcxNTMyMzk4MjQyLCJsYW5nIjoiemhfQ04iLCJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsiMCI6eyJhY2Nlc3NUeXBlIjoxLCJtZW1iZXJJZCI6MjI0NDQ2Mzk5MywidGd0SWQiOiIxbU1TdGgtUkdUVVV6V1BiTXZ3VFRsQSJ9fX19", "_cc_": "Vq8l%2BKCLiw%3D%3D", "_l_g_": "Ug%3D%3D", "_nk_": "%5Cu7EBF%5Cu5B9D%5Cu7CD6", "cookie1": "WvAz3%2B%2F06gFSlBN6ZZ7Wjm49P%2B47S3hfQjk5juF44Qk%3D", "cookie17": "UUplZfR9fbZ6Kw%3D%3D", "dnk": "%5Cu7EBF%5Cu5B9D%5Cu7CD6", "existShop": "MTU3MTUzMjM5OA%3D%3D", "lgc": "%5Cu7EBF%5Cu5B9D%5Cu7CD6", "sg": "%E7%B3%963e", "skt": "9b42a515e1003082", "tg": "0", "tracknick": "%5Cu7EBF%5Cu5B9D%5Cu7CD6", "uc1": "existShop=false&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&pas=0&cookie15=W5iHLLyFOGW7aA%3D%3D&cookie21=W5iHLLyFeYZ1WM9hVnmS&lng=zh_CN&tag=8&cookie14=UoTbnKZQZLcmTw%3D%3D", "uc3": "vt3=F8dByucnLD9gZJVdG7g%3D&nk2=rNXZxyRF&lg2=URm48syIIVrSKA%3D%3D&id2=UUplZfR9fbZ6Kw%3D%3D", "uc4": "id4=0%40U2gvKn5ZKc4v9nFwtBf%2BA8qWkWFT&nk4=0%40rvvw8H3AM%2FDsXOdA3SNzJjA%3D", "unb": "2244463993", "XSRF-TOKEN": "9082e875-5cc8-4a93-b61b-eb7b6e8c560e"}
for key, value in cookies_dict.items():
    cookies += key + '=' + value + ';'

print(cookies)
print('t=2f510904a1652b167e5690ddded736a2; enc=lT3GLDXH6Pa04EkYdmlDiCaP6Mt7T7p4zxSyC9NtzXVUSWJwYdjVSFGsa63XvKNLVzehDcZV8t08S%2FjnZEB8Ow%3D%3D; mt=ci=0_0; thw=cn; cookie2=161967b44afa5f1d899d4e5e7fb5d65c; _tb_token_=53e3a678eee19; cna=vny+FSuWBxsCAT2emPgYK1Ms; v=0; miid=213872151114548654; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5hmAEwUWMJdCV%2BTpmn3Ct4JuwaHGndnn098BOcf7m3jOhqgYts2WEiVJ7AytBrmjrk4DIlzg9Ing%2B5l6ZMDQcDp1Kwu5pQLTWFW1ACcbCIaXOgcQCNFdbCF53OyhQCw6sd3tYZSPD%2B2mWbkTPOHzONSAnD8tkwKgoi4UkBlS%2FwhMR6yWoz%2FrWDcR2ZEDP3pWaa%2F1CUIatD8xatnw%2FZsfaxNuIJFd1kf5WjLaPpULGX6omeWSq%2BY4ltT1i%2Ft; _m_h5_tk=a4f0fc2fe3e503a810cc1a110a3d0d50_1571492643068; _m_h5_tk_enc=7d42ed9081ba4d15ba8d08f50b4e4647; l=dBgG34Yuq6A0JznSBOfgcuI8aB_teCdf1sPzw4_g9ICPOo1c0VeRWZIaNf8kCnGVnsTXJ3RF8Ep7BfTaByUBR-ERwSlBs2JZndLh.; isg=BF9fbK0GfrxSz3qsAitdZo6Q7rMpbLPpfmhomPGpTI_FgHwC-Je1tmMSQlBbGIve')
headers = {
    # 'Proxy-Authorization': 'Basic ' + appKey,
    # 'Referer': 'https://item.taobao.com/item.htm?spm=a219r.lm874.14.103.5c134edcn1NCzw&id=573438501591&ns=1&abbucket=7',
    'Referer': 'https://item.taobao.com/item.htm?spm=a219r.lm874.14.103.5c134edcn1NCzw&id=573438501591&ns=1&abbucket=7',
    'cookie': 't=2f510904a1652b167e5690ddded736a2; enc=lT3GLDXH6Pa04EkYdmlDiCaP6Mt7T7p4zxSyC9NtzXVUSWJwYdjVSFGsa63XvKNLVzehDcZV8t08S%2FjnZEB8Ow%3D%3D; mt=ci=0_0; thw=cn; cookie2=161967b44afa5f1d899d4e5e7fb5d65c; _tb_token_=53e3a678eee19; cna=vny+FSuWBxsCAT2emPgYK1Ms; v=0; miid=213872151114548654; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5hmAEwUWMJdCV%2BTpmn3Ct4JuwaHGndnn098BOcf7m3jOhqgYts2WEiVJ7AytBrmjrk4DIlzg9Ing%2B5l6ZMDQcDp1Kwu5pQLTWFW1ACcbCIaXOgcQCNFdbCF53OyhQCw6sd3tYZSPD%2B2mWbkTPOHzONSAnD8tkwKgoi4UkBlS%2FwhMR6yWoz%2FrWDcR2ZEDP3pWaa%2F1CUIatD8xatnw%2FZsfaxNuIJFd1kf5WjLaPpULGX6omeWSq%2BY4ltT1i%2Ft; _m_h5_tk=a4f0fc2fe3e503a810cc1a110a3d0d50_1571492643068; _m_h5_tk_enc=7d42ed9081ba4d15ba8d08f50b4e4647; l=dBgG34Yuq6A0JznSBOfgcuI8aB_teCdf1sPzw4_g9ICPOo1c0VeRWZIaNf8kCnGVnsTXJ3RF8Ep7BfTaByUBR-ERwSlBs2JZndLh.; isg=BF9fbK0GfrxSz3qsAitdZo6Q7rMpbLPpfmhomPGpTI_FgHwC-Je1tmMSQlBbGIve',
    # 'cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

# for i in range(1, 101):
#     url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=573438501591&userNumId=2242712302&currentPageNum={0}&pageSize=100&orderType=sort_weight&hasSku=false&folded=0&callback=jsonp_tbcrate_reviews_list'.format(i)
#     try:
#         # res = requests.get(url, headers=headers, proxies=proxy, verify=False)
#         res = requests.get(url, headers=headers, verify=False)
#         print(res.text)
#         print(i)
#         time.sleep(12)
#     except Exception as e:
#         print(e)



