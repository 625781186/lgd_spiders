import requests

url = 'https://www.qichacha.com/firm_3f21f20b70e4509bc80374c744a4c02d.html'

headers = {
    'Host': 'www.qichacha.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

res = requests.get(url, headers=headers)
print(res.text)