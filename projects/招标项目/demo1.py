# url = http://www.bidchance.com/freesearch.do?filetype=&channel=gonggao&currentpage=1&searchtype=sj&queryword=&displayStyle=title&pstate=&field=all&leftday=&province=&bidfile=&project=&heshi=&recommend=&field=all&jing=&starttime=&endtime=&attachment=

import requests
import execjs
import re

# url = 'http://www.bidchance.com/freesearch.do?filetype=&channel=gonggao&currentpage=1&searchtype=sj&queryword=&displayStyle=title&pstate=&field=all&leftday=&province=&bidfile=&project=&heshi=&recommend=&field=all&jing=&starttime=&endtime=&attachment='
url = 'http://www.bidchance.com/freesearch.do?filetype=&channel=gonggao&currentpage=1&searchtype=sj&queryword=&displayStyle=title&pstate=&field=all&leftday=&province=&bidfile=&project=&heshi=&recommend=&field=all&jing=&starttime=&endtime=&attachment='

headers = {
    'Cookie': '__jsluid_h=c1d8aed5ea55630cffd3e5297c34412a; __jsl_clearance=1568634132.784|0|ZgkxLQqvkNglT6Ve1MLjXWeLowM%3D; reg_referer="aHR0cDovL3d3dy5iaWRjaGFuY2UuY29tL3Nlby93ZWIxMjQ3NTU0MDc1Lmh0bWw="; Hm_lvt_2751005a6080efb2d39109edfa376c63=1568634136; JSESSIONID=74E88179DE14129623FAE0294AF220B5; Hm_lpvt_2751005a6080efb2d39109edfa376c63=1568634585',
    'Host': 'www.bidchance.com',
    'Referer': 'http://www.bidchance.com/freesearch.do?filetype=&channel=gonggao&currentpage=2&searchtype=sj&queryword=&displayStyle=title&pstate=&field=all&leftday=&province=&bidfile=&project=&heshi=&recommend=&field=all&jing=&starttime=&endtime=&attachment=',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

res = requests.get(url, headers=headers)
print(res.text)
# print(type(res.text))

# html = res.text.replace('<script>', '').replace('</script>', '')
# print(html)
# print(execjs.eval(html))

# pat1 = re.compile(r'var x="(.*?),y=', re.S | re.M)
# pat2 = re.compile(r'y="(.*?)",f=func', re.S | re.M)
# pat3 = re.compile(r'}",(.*?)</script>', re.S | re.M)
#
# x = pat1.findall(res.text)[0]
# print(x)
# y = pat2.findall(res.text)[0]
# print(y)
# func = pat3.findall(res.text)[0]
# print(func)
# js_func = execjs.compile(res.text)
# js_func.call('function(x,y)', x, y)
