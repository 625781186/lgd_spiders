
import requests
import time
import random
url = 'https://www.tianyancha.com/pagination/invest.xhtml?ps=20&pn=1&id=3053723260&_=1568796335332'

headers = {
    'Cookie':'jsid=SEM-BAIDU-PZ1907-SY-000100; TYCID=97d228b0c7c811e9b81d4bfe21ed2dc9; undefined=97d228b0c7c811e9b81d4bfe21ed2dc9; ssuid=9498838220; _ga=GA1.2.2055685819.1566800006; aliyungf_tc=AQAAAOlaQhE9rwUAaxrAAVX4FpoJqNDB; csrfToken=zuCDmOAx4vfYxsqa8jEVeYiY; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25221%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2590%2589%25E5%25A8%259C%25C2%25B7%25E6%2588%25B4%25E7%25BB%25B4%25E6%2596%25AF%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A0%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522new%2522%253A%25221%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNjYzODEyNDEyOSIsImlhdCI6MTU2ODY5ODU2MiwiZXhwIjoxNjAwMjM0NTYyfQ.cU3C74AjRJhyt2gx6SCQs1UgAXrUy1lTTTr8MyDKLJGCp6i0qqdRjp8H9TcKg969ZO3Gn_z7GroctI_XZ2zM6Q%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252216638124129%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNjYzODEyNDEyOSIsImlhdCI6MTU2ODY5ODU2MiwiZXhwIjoxNjAwMjM0NTYyfQ.cU3C74AjRJhyt2gx6SCQs1UgAXrUy1lTTTr8MyDKLJGCp6i0qqdRjp8H9TcKg969ZO3Gn_z7GroctI_XZ2zM6Q; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568613367,1568629073,1568698494,1568795737; _gid=GA1.2.1652575834.1568795738; RTYCID=5854805381564e6c836973539b52adda; CT_TYCID=9ed92b9b3197401ea404995a4218846a; bannerFlag=true; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568796337; _gat_gtag_UA_123487620_1=1; cloud_token=79a28032d829478696670fe050942dd4; cloud_utm=3d92efd52d124469bab626a5feb7deb6',
    'Host': 'www.tianyancha.com',
    'Referer': 'https://www.tianyancha.com/company/3053723260',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

for i in range(17):
    url = 'https://www.tianyancha.com/pagination/invest.xhtml?ps=20&pn=%s&id=3053723260&_=%s'%(i+1, 1568797502000 + 2*i)
    # print(url)
    res = requests.get(url, headers=headers)
    print(res.content)
    print(res.url)
    print('================')
    time.sleep(random.random() * 8)
