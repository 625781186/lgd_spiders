# !/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/19 11:45
# @Author  : lgd
# @Project : lgd-Crawler
# @File    : 连衣裙.py
# /***
 
import requests
from selenium import webdriver
import time

url = 'https://s.taobao.com/search?spm=a21bo.2017.201856-fline.1.5af911d9KHFWh2&q=%E8%BF%9E%E8%A1%A3%E8%A3%99&refpid=420460_1006&source=tbsy&style=grid&tab=all&pvid=d0f2ec2810bcec0d5a16d5283ce59f66'

headers = {
    'cookie': 'mt=ci%3D-1_0; thw=cn; UM_distinctid=16aba0a5e78719-09431e07700053-353166-15f900-16aba0a5e7967a; hng=CN%7Czh-CN%7CCNY%7C156; miid=1418458630497981324; t=40273bb2291930402247da8849b8cae5; cna=Yq3PFZK6WC4CAXug4Taxi4fA; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zZPEr%2FCrvCMS%2BG3sTRRWrQ%2BVVTl09ME1KrXE17iYYltIdiowM11Qrbdv11%2FucF7%2FR86HELyqnwHJ6i2m3XI18KuDH%2FxCy7QOhz6o6yLr67KsqDAQSjpaMIDT7%2FY1XKdtJahVbkwSrpCjyNq8j%2FfTi114i0zlOnf1fCORUIsW0r9CrBu347YarDLHojvktjnFI%2BtBTE188WS3zxOR%2B026ebm5GkAd6I3oxVGi959JCx%2FAVAJpYFXkujAN1GfhaF4%2FWBwLUpCF6G5TyKziVToH7YopuvLRokl7mku9QvyN1HuoE6febiim2U8BSWGz4%3D; cookie2=1afd3183469648f38f05b65580bd7193; v=0; _tb_token_=74e564eeed349; _m_h5_tk=f6617d19d906e1d1ff34100c8b1b1702_1566191010997; _m_h5_tk_enc=c453ee38cfbfaafb0c09c1589bef1eec; unb=2244463993; uc3=nk2=rNXZxyRF&id2=UUplZfR9fbZ6Kw%3D%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dBy3K1HccGLmhlpTE%3D; csg=c1298f9a; lgc=%5Cu7EBF%5Cu5B9D%5Cu7CD6; cookie17=UUplZfR9fbZ6Kw%3D%3D; dnk=%5Cu7EBF%5Cu5B9D%5Cu7CD6; skt=9bca0c05a82567cd; existShop=MTU2NjE4NjIwOQ%3D%3D; tracknick=%5Cu7EBF%5Cu5B9D%5Cu7CD6; _cc_=URm48syIZQ%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=%E7%B3%963e; _nk_=%5Cu7EBF%5Cu5B9D%5Cu7CD6; cookie1=WvAz3%2B%2F06gFSlBN6ZZ7Wjm49P%2B47S3hfQjk5juF44Qk%3D; mt=ci=51_1; enc=XBm1GB%2FdMGQp29SMi7DoZEm38rUHix8obsA9vWxXDAR3EhIbQrZAz%2BLWsokObDBcwW%2FLfgBkozn3cFMqNGR8aA%3D%3D; JSESSIONID=D8D75A6044EA098FA3AAB40E25B24628; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=UIHiLt3xThH8t7YQoFNq&cookie15=VT5L2FSpMGV7TQ%3D%3D&existShop=false&pas=0&cookie14=UoTaHoqcw%2BYN%2Fg%3D%3D&tag=8&lng=zh_CN; swfstore=184110; whl=-1%260%260%260; l=cBgvOn7mqUL4Lw4QBOCMZuIR54_OLIRAguPRw1X2i_5C568MYO_OkRPfgFJ6cjWdOcTB4aVvW6J9-etkmCX_Ju--g3fP.; isg=BHJyqvQfe9fDZ0f509lzxqmOw7iUq3sDYvC9rDxLwCUCzxLJJJfFrY0tuytWv-41; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0',
    'referer': 'https://www.taobao.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
}


driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
print(driver.page_source)

# res = requests.get(url, headers=headers, verify=False)
# print(res.text)


