import requests
from lxml import etree

url = 'https://www.qichacha.com/gongsi_area.html'

headers = {
    'Host': 'www.qichacha.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

for i in range(1000):
    params = {
        'prov': 'BJ',
        'city': '110101',
        'p': i + 1,
    }

    res = requests.get(url, headers=headers, params=params)
    # print(res.text)
    html = etree.HTML(res.text)
    infos = html.xpath('//*[@id="searchlist"]/table/tbody/tr')
    print(len(infos))
    for j in infos:
        title = j.xpath('./td[2]/a//text()')
        owner = j.xpath('.//a[@class="a-blue"]/text()')
        address = j.xpath('./td[2]/p[3]/text()')
        cmp_url = j.xpath('./td[2]/a/@href')
        print(title)
        print(owner)
        print(address)
        print(cmp_url)
        print('-----------------')
    print('=='*30)