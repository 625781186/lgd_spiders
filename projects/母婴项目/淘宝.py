# !/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/19 10:32
# @Author  : lgd
# @Project : lgd-Crawler
# @File    : 淘宝.py
# /***

from lxml import etree
import requests


url = 'https://re.taobao.com/search?clk1=&p4pTags=&ismall=&refpos=&refpid=421019_1006&keyword=%E6%AF%8D%E5%A9%B4%E7%94%A8%E5%93%81&_input_charset=utf-8&page=0&isinner=0'

headers = {
    'cookie': 'mt=ci%3D-1_0; thw=cn; UM_distinctid=16aba0a5e78719-09431e07700053-353166-15f900-16aba0a5e7967a; hng=CN%7Czh-CN%7CCNY%7C156; miid=1418458630497981324; t=40273bb2291930402247da8849b8cae5; cna=Yq3PFZK6WC4CAXug4Taxi4fA; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zZPEr%2FCrvCMS%2BG3sTRRWrQ%2BVVTl09ME1KrXE17iYYltIdiowM11Qrbdv11%2FucF7%2FR86HELyqnwHJ6i2m3XI18KuDH%2FxCy7QOhz6o6yLr67KsqDAQSjpaMIDT7%2FY1XKdtJahVbkwSrpCjyNq8j%2FfTi114i0zlOnf1fCORUIsW0r9CrBu347YarDLHojvktjnFI%2BtBTE188WS3zxOR%2B026ebm5GkAd6I3oxVGi959JCx%2FAVAJpYFXkujAN1GfhaF4%2FWBwLUpCF6G5TyKziVToH7YopuvLRokl7mku9QvyN1HuoE6febiim2U8BSWGz4%3D; cookie2=1afd3183469648f38f05b65580bd7193; v=0; _tb_token_=74e564eeed349; _m_h5_tk=f6617d19d906e1d1ff34100c8b1b1702_1566191010997; _m_h5_tk_enc=c453ee38cfbfaafb0c09c1589bef1eec; uc1=cookie14=UoTaHoqcxJKaQQ%3D%3D; ctoken=NBOT-Vj5PbUKV4K3-b1gZPkn; mt=ci%3D-1_0; l=cBgvOn7mqUL4Lt_FKOfgVuIR54_OgQAbzsPzw41gdIBOTT4kWKUg2HwIZ_xim3_9XNWFGPYB4aVvW6JT0U0_Jyt0Tuo-AaZTWaf..; isg=BDs7NWMh4hgzxt6-okq6OagNyh9lOEIMg1PEKy36CjpKjFlutWXC4oaAomxnrKeK',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'referer': 'https://re.taobao.com/action_ecpm_home?ali_trackid=19_642b244bfcce86493e590fffabf39968&spm=a21bo.2017.201862-3.1',
}

res = requests.get(url, headers=headers, verify=False)
# print(res.text)
html = etree.HTML(res.text)
ls = html.xpath('//div[@id="J_waterfallWrapper"]/div[@class="item"]')
print(len(ls))
for i in ls:
    url = i.xpath('./a/@href')[0]
    title = i.xpath('.//span[@class="title"]/text()')[0]
    print(url)
    print(title)
    print('===================')



