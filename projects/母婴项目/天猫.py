# !/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 8:30
# @Author  : lgd
# @Project : lgd-Crawler
# @File    : 天猫.py
# /***

import time
import random
import requests
from lxml import etree
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

base_url = 'https://list.tmall.com/search_product.htm'
for i in range(5):
    params = {
        'spm': 'a220m.1000858.1000724.10.1bb07695ZUcFyS',
        's': i * 60,
        'q': '(unable to decode value)',
        'sort': 's',
        'style': 'g',
        'from': '..pc_1_suggest',
        'suggest': '0_9',
        'active': '1',
        'smAreaId': '410100',
        'type': 'pc',
    }

    url = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.10.1bb07695ZUcFyS&s={0}&q=%C1%AC%D2%C2%C8%B9%B4%BA%C7%EF&sort=s&style=g&from=..pc_1_suggest&suggest=0_9&active=1&smAreaId=410100&type=pc'.format(i * 60)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'cookie': 'hng=CN%7Czh-CN%7CCNY%7C156; _med=dw:1600&dh:900&pw:1600&ph:900&ist:0; sm4=410100; cna=Yq3PFZK6WC4CAXug4Taxi4fA; tk_trace=1; t=40273bb2291930402247da8849b8cae5; tracknick=%5Cu7EBF%5Cu5B9D%5Cu7CD6; lid=%E7%BA%BF%E5%AE%9D%E7%B3%96; lgc=%5Cu7EBF%5Cu5B9D%5Cu7CD6; enc=XBm1GB%2FdMGQp29SMi7DoZEm38rUHix8obsA9vWxXDAR3EhIbQrZAz%2BLWsokObDBcwW%2FLfgBkozn3cFMqNGR8aA%3D%3D; _tb_token_=e6fe515ab038b; cookie2=10238fd87ea4e171f26713c5c8e90d83; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=231497; dnk=%5Cu7EBF%5Cu5B9D%5Cu7CD6; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=UIHiLt3xThH8t7YQoFNq&cookie15=VT5L2FSpMGV7TQ%3D%3D&existShop=false&pas=0&cookie14=UoTaHogtfxM%2BdA%3D%3D&tag=8&lng=zh_CN; uc3=lg2=Vq8l%2BKCLz3%2F65A%3D%3D&vt3=F8dBy3K7l0zAs6kmPdQ%3D&id2=UUplZfR9fbZ6Kw%3D%3D&nk2=rNXZxyRF; uc4=id4=0%40U2gvKn5ZKc4v9nFwtBbXU9NGXlbu&nk4=0%40rvvw8H3AM%2FDsXX842kbp9MY%3D; _l_g_=Ug%3D%3D; unb=2244463993; cookie1=WvAz3%2B%2F06gFSlBN6ZZ7Wjm49P%2B47S3hfQjk5juF44Qk%3D; login=true; cookie17=UUplZfR9fbZ6Kw%3D%3D; _nk_=%5Cu7EBF%5Cu5B9D%5Cu7CD6; sg=%E7%B3%963e; csg=7c3daaa2; _m_h5_tk=1f0a768ec4f120407567c734f5e19c2f_1566375949820; _m_h5_tk_enc=d1702a6d00acaaf7851e428272d54899; tt=tmall-main; pnm_cku822=098%23E1hvFvvUvbpvUpCkvvvvvjiPRFdW0jnhRLMp0jD2PmPv0j1HPFd9tjlhP2Myzji8PuwCvvpvvUmmmphvLCv5A9vjcRClKWVTKo9vD7zhaXp7Ecqh6jc6%2BulAbqk1DfesRk9hD7zhaXTAVAdpaNFgjCODN%2BLpaNpXe5xLD7zhaB4AVArlYPexdXkEvpvVmvvC9jaCuphvmvvv92fA8E6EKphv8vvvvvCvpvvvvvv2UhCv2HpvvvW9phvWh9vvvACvpv11vvv2UhCv2jhCvpvVvvpvvhCv2QhvCvvvMMGtvpvhvvvvvv%3D%3D; res=scroll%3A1583*5976-client%3A1583*789-offset%3A1583*5976-screen%3A1600*900; cq=ccp%3D0; whl=-1%260%260%260; l=cBQQKpJVv7W7TCAEBOCMNuIR54_OMIRAguPRw1X2i_5Ce_T1E9bOkJQ3uE96cjWdOj8p4aVvW6J9-etljNB2PjhHtBUV.; isg=BKurdCDacq7K-69N6TutQdhVOs9VaLLc8yNUmx0o-upBvMsepJBkkktWFrx3nBc6; x=__ll%3D-1%26_ato%3D0',
        'referer': url
    }

    res = requests.get(url, headers=headers, params=params, verify=False)
    print('当前页码：', i + 1)
    # print(res.text)
    html = etree.HTML(res.text)
    ls = html.xpath('//div[@id="J_ItemList"]/div[@class="product  "]')
    for j in ls:
        title = j.xpath('.//p[@class="productTitle"]/a/@title')[0]
        price = j.xpath('.//p[@class="productPrice"]/em/@title')[0]
        shop = j.xpath('.//div[@class="productShop"]/a/text()')[0].replace('\n', '')
        sales_volume = j.xpath('.//p[@class="productStatus"]//em/text()')[0]
        comment_volume = j.xpath('.//p[@class="productStatus"]/span[2]/a/text()')[0]
        detail_url = 'https:' + j.xpath('.//p[@class="productTitle"]/a/@href')[0]
        print(title)
        print(price)
        print(shop)
        print(sales_volume)
        print(comment_volume)
        print(detail_url)
        # driver.get(detail_url)
        # driver.delete_all_cookies()
        # cookies = {
        #     'hng': 'CN%7Czh-CN%7CCNY%7C156',
        #     '_med': 'dw:1600&dh:900',
        #     'pw': '1600',
        #     'ph':'900',
        #     'ist':'0',
        #     'cq':'ccp%3D1',
        #     'sm4': '410100',
        #     'cna': 'Yq3PFZK6WC4CAXug4Taxi4fA',
        #     'tk_trace': '1',
        #     't': '40273bb2291930402247da8849b8cae5',
        #     'uc3': 'nk2=rNXZxyRF',
        #     'id2': 'UUplZfR9fbZ6Kw%3D%3D',
        #     'lg2': 'WqG3DMC9VAQiUQ%3D%3D',
        #     'vt3': 'F8dBy3K1HccGLmhlpTE%3D',
        #     'tracknick': '%5Cu7EBF%5Cu5B9D%5Cu7CD6',
        #     'lid': '%E7%BA%BF%E5%AE%9D%E7%B3%96',
        #     'lgc': '%5Cu7EBF%5Cu5B9D%5Cu7CD6',
        #     'enc': 'XBm1GB%2FdMGQp29SMi7DoZEm38rUHix8obsA9vWxXDAR3EhIbQrZAz%2BLWsokObDBcwW%2FLfgBkozn3cFMqNGR8aA%3D%3D',
        #     '_tb_token_': 'e6fe515ab038b',
        #     'cookie2': '10238fd87ea4e171f26713c5c8e90d83',
        #     '_m_h5_tk': 'bfa7f799903b4aec93bd229405f4f0a6_1566357408989',
        #     '_m_h5_tk_enc': '66ca8e081d4485282b9e830976308fb7',
        #     'tt': 'nvzhuang.tmall.com',
        #     'otherx': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0',
        #     'swfstore':'231497',
        #     'res':'scroll%3A1583*5976-client%3A1583*150-offset%3A1583*5976-screen%3A1600*900',
        #     'pnm_cku822': '098%23E1hv%2B9vUvbpvU9CkvvvvvjiPRFdW6j1RPFqh6jljPmPv6jiEn2My0jrRPsSOzjYnPsItvpvhvvvvvvGCvvLMMQvvmphvLCvgaQvj8txrgj7Jymx%2FAj7QiXTAVAnlMWLUjE3gp%2BLUlnQfHFXXiXVvQE01Ux8x9WLZjLyDZacEKOmAdcHUa4A%2B%2BboJa6Mpgb2XrqoEvpvVmvvC9jaCuphvmvvv92f1OjWoKphv8vvvvvCvpvvvvvv2UhCvvHIvvvW9phvWh9vvvACvpv11vvv2UhCv2jhCvpvVvmvvvhCviQhvCvvv9UU%3D',
        #     'isg': 'BFJSD_xVW7Eo4qb6qHh0rskmoxj0y1tjQpCdTByp8YSUL_MpBPb4DUwJn8u2X86V',
        #     'l': 'cBQQKpJVv7W7TeR3BOfNNuIR54_OmQRb8sPzw41gdIB19X1_fdC6DHwIGvOpd3QQE9fnqetPrSLOTdnXrEzdgjVWuEhBe82O',
        # }
        # driver.get('https://www.tmall.com/?spm=a220o.1000855.a2226mz.1.29075eaeQrbnuk')
        driver.get(detail_url)
        cookies = {
            'hng': 'CN%7Czh-CN%7CCNY%7C156',
            '_med': 'dw:1600',
            'dh': '900',
            'pw': '1600',
            'ph': '900',
            'ist': '0',
            'sm4': '410100',
            'cna': 'Yq3PFZK6WC4CAXug4Taxi4fA',
            'tk_trace': '1',
            't': '40273bb2291930402247da8849b8cae5',
            'tracknick': '%5Cu7EBF%5Cu5B9D%5Cu7CD6',
            'lid': '%E7%BA%BF%E5%AE%9D%E7%B3%96',
            'lgc': '%5Cu7EBF%5Cu5B9D%5Cu7CD6',
            'enc': 'XBm1GB%2FdMGQp29SMi7DoZEm38rUHix8obsA9vWxXDAR3EhIbQrZAz%2BLWsokObDBcwW%2FLfgBkozn3cFMqNGR8aA%3D%3D',
            '_tb_token_': 'e6fe515ab038b',
            'cookie2': '10238fd87ea4e171f26713c5c8e90d83',
            'otherx': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0',
            'swfstore': '231497',
            'dnk': '%5Cu7EBF%5Cu5B9D%5Cu7CD6',
            'uc1': 'V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D',
            'cookie16': 'V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D',
            'cookie21': 'UIHiLt3xThH8t7YQoFNq',
            'cookie15': 'VT5L2FSpMGV7TQ%3D%3D',
            'existShop': 'false',
            'pas': '0',
            'cookie14': 'UoTaHogtfxM%2BdA%3D%3D',
            'tag': '8',
            'lng': 'zh_CN',
            'uc3': 'Vq8l%2BKCLz3%2F65A%3D%3D',
            'lg2': 'Vq8l%2BKCLz3%2F65A%3D%3D',
            'vt3': 'F8dBy3K7l0zAs6kmPdQ%3D',
            'id2': 'UUplZfR9fbZ6Kw%3D%3D&',
            'nk2': 'rNXZxyRF',
            'uc4': '0%40U2gvKn5ZKc4v9nFwtBbXU9NGXlb',
            'id4': '0%40U2gvKn5ZKc4v9nFwtBbXU9NGXlbu',
            'nk4': '0%40rvvw8H3AM%2FDsXX842kbp9MY%3D',
            '_l_g_': 'Ug%3D%3D',
            'unb': '2244463993',
            'cookie1': 'WvAz3%2B%2F06gFSlBN6ZZ7Wjm49P%2B47S3hfQjk5juF44Qk%3D',
            'login': 'true',
            'cookie17': 'UUplZfR9fbZ6Kw%3D%3D',
            '_nk_': '%5Cu7EBF%5Cu5B9D%5Cu7CD6',
            'sg': '%E7%B3%963e',
            'csg': '7c3daaa2',
            '_m_h5_tk': '1f0a768ec4f120407567c734f5e19c2f_1566375949820',
            '_m_h5_tk_enc': 'd1702a6d00acaaf7851e428272d54899',
            'tt': 'tmall-main',
            'pnm_cku822': '098%23E1hvFvvUvbpvUpCkvvvvvjiPRFdW0jnhRLMp0jD2PmPv0j1HPFd9tjlhP2Myzji8PuwCvvpvvUmmmphvLCv5A9vjcRClKWVTKo9vD7zhaXp7Ecqh6jc6%2BulAbqk1DfesRk9hD7zhaXTAVAdpaNFgjCODN%2BLpaNpXe5xLD7zhaB4AVArlYPexdXkEvpvVmvvC9jaCuphvmvvv92fA8E6EKphv8vvvvvCvpvvvvvv2UhCv2HpvvvW9phvWh9vvvACvpv11vvv2UhCv2jhCvpvVvvpvvhCv2QhvCvvvMMGtvpvhvvvvvv%3D%3D',
            'res': 'scroll%3A1583*5976-client%3A1583*789-offset%3A1583*5976-screen%3A1600*900',
            'cq': 'ccp%3D0',
            'whl': '-1%260%260%260',
            'l': 'cBQQKpJVv7W7TCAEBOCMNuIR54_OMIRAguPRw1X2i_5Ce_T1E9bOkJQ3uE96cjWdOj8p4aVvW6J9-etljNB2PjhHtBUV',
            'isg': 'BKurdCDacq7K-69N6TutQdhVOs9VaLLc8yNUmx0o-upBvMsepJBkkktWFrx3nBc6',
            'x': '__ll%3D-1%26_ato%3D0',
        }
        driver.delete_all_cookies()
        for i, j in cookies.items():
            driver.add_cookie({'name': i, 'value': j})
        driver.get(url)
        time.sleep(3)
        # driver.get(detail_url)


        # for k in cookies:
        # driver.add_cookie('hng=CN%7Czh-CN%7CCNY%7C156; _med=dw:1600&dh:900&pw:1600&ph:900&ist:0; cq=ccp%3D1; sm4=410100; cna=Yq3PFZK6WC4CAXug4Taxi4fA; tk_trace=1; t=40273bb2291930402247da8849b8cae5; uc3=nk2=rNXZxyRF&id2=UUplZfR9fbZ6Kw%3D%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dBy3K1HccGLmhlpTE%3D; tracknick=%5Cu7EBF%5Cu5B9D%5Cu7CD6; lid=%E7%BA%BF%E5%AE%9D%E7%B3%96; lgc=%5Cu7EBF%5Cu5B9D%5Cu7CD6; enc=XBm1GB%2FdMGQp29SMi7DoZEm38rUHix8obsA9vWxXDAR3EhIbQrZAz%2BLWsokObDBcwW%2FLfgBkozn3cFMqNGR8aA%3D%3D; _tb_token_=e6fe515ab038b; cookie2=10238fd87ea4e171f26713c5c8e90d83; _m_h5_tk=bfa7f799903b4aec93bd229405f4f0a6_1566357408989; _m_h5_tk_enc=66ca8e081d4485282b9e830976308fb7; tt=nvzhuang.tmall.com; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=231497; res=scroll%3A1583*5976-client%3A1583*150-offset%3A1583*5976-screen%3A1600*900; pnm_cku822=098%23E1hv%2B9vUvbpvU9CkvvvvvjiPRFdW6j1RPFqh6jljPmPv6jiEn2My0jrRPsSOzjYnPsItvpvhvvvvvvGCvvLMMQvvmphvLCvgaQvj8txrgj7Jymx%2FAj7QiXTAVAnlMWLUjE3gp%2BLUlnQfHFXXiXVvQE01Ux8x9WLZjLyDZacEKOmAdcHUa4A%2B%2BboJa6Mpgb2XrqoEvpvVmvvC9jaCuphvmvvv92f1OjWoKphv8vvvvvCvpvvvvvv2UhCvvHIvvvW9phvWh9vvvACvpv11vvv2UhCv2jhCvpvVvmvvvhCviQhvCvvv9UU%3D; isg=BFJSD_xVW7Eo4qb6qHh0rskmoxj0y1tjQpCdTByp8YSUL_MpBPb4DUwJn8u2X86V; l=cBQQKpJVv7W7TeR3BOfNNuIR54_OmQRb8sPzw41gdIB19X1_fdC6DHwIGvOpd3QQE9fnqetPrSLOTdnXrEzdgjVWuEhBe82O.')
        # driver.execute_script('return d.innerHTML = "\uff08" + i + "\u4eba\u6c14\uff09";')
        # mycookie = driver.get_cookies()
        # for l in mycookie:
        #     print(l)
        # detail_html = driver.page_source
        # detail_res = requests.get(detail_url, headers=headers, verify=False)
        # detail_html = etree.HTML(driver.page_source)
        # print(detail_html)
        # collection_volume = detail_html.xpath('//span[@id="J_CollectCount"]/text()')
        # print(collection_volume)
        # driver.implicitly_wait(10)
        # try:
        #     element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.ID, "J_CollectCount"))
        # except:
        #     print('元素等待失败')

        print(driver.page_source)
        # collection_volume = detail_html.xpath('//span[@id="J_CollectCount"]/text()')
        # print(collection_volume)

        time.sleep(random.random() * 5)
        print('--------------------------')
        # driver.close()
    print('===='*25)
    time.sleep(random.random() * 5)




