# -*- coding: utf-8 -*-
# @Time    : 2019/9/23 16:50
# @Author  : LGD
# @File    : taobao_detailpage.py
# @功能    : 爬取淘宝详情页信息

# 引入自带模块或第三方模块
import requests

url = 'https://detail.tmall.com/item.htm?id=600049973655&ns=1&abbucket=8'

headers = {
    'cookie': 't=a3dfe14b119e11b663a04fe50b7be16b; cna=vny+FSuWBxsCAT2emPgYK1Ms; thw=cn; miid=1447653216300413215; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=6a10afc0f9032c6aa65abc22236572b5_1568786847167; _m_h5_tk_enc=d779d41504d4d77a4567ce01a1f0d35b; v=0; cookie2=1dc5c41c1a58c067176c4362bfcfb24b; _tb_token_=e63ef378b7833; unb=2244463993; uc3=lg2=VT5L2FSpMGV7TQ%3D%3D&id2=UUplZfR9fbZ6Kw%3D%3D&nk2=rNXZxyRF&vt3=F8dByuK0%2B6sACGuN4ZQ%3D; csg=f268f6c4; lgc=%5Cu7EBF%5Cu5B9D%5Cu7CD6; cookie17=UUplZfR9fbZ6Kw%3D%3D; dnk=%5Cu7EBF%5Cu5B9D%5Cu7CD6; skt=0b072e98d4de2bab; existShop=MTU2OTA1ODgzMA%3D%3D; uc4=id4=0%40U2gvKn5ZKc4v9nFwtBbYACcNl3NK&nk4=0%40rvvw8H3AM%2FDsXXDYQVZcsEI%3D; tracknick=%5Cu7EBF%5Cu5B9D%5Cu7CD6; _cc_=URm48syIZQ%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=%E7%B3%963e; _nk_=%5Cu7EBF%5Cu5B9D%5Cu7CD6; cookie1=WvAz3%2B%2F06gFSlBN6ZZ7Wjm49P%2B47S3hfQjk5juF44Qk%3D; enc=ROW7Hu54PBKvnRmwmGtuRFYaFEv%2B5cM31eQ47jHA5ew5AF6uJvzYu%2FmOV56k6txhYFecMXw%2B1Nr%2B2TCStNsUcQ%3D%3D; mt=ci=51_1; swfstore=116521; whl=-1%260%260%260; JSESSIONID=6EA307B72F0D27451E07E240CA1EE555; l=dBOPCDN7qJtDdeZBBOfNRurza77t6Idf1sPzaNbMiICPOT5y_cAFWZC7PNY2CnGVnssv537el_8YB7Y3PPa9CfRqnoYCgsDKndLh.; isg=BOnpz1kjkJ1HbKzPuBQboNki-JVDtt3ohOV0o4vfkVC2Ugpk1wfVusRIFLZBSnUg; uc1=cookie14=UoTaEcGTehzpDw%3D%3D&lng=zh_CN&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&existShop=false&cookie21=WqG3DMC9Fb5mPLIQo9kR&tag=8&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&pas=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0',
    'referer': 'https://s.taobao.com/list?spm=a217f.8051907.312344.1.36633308oONmtx',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

res = requests.get(url, headers=headers)
print(res.text)
