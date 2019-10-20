import requests

url = 'https://www.tianyancha.com/company/3053723260'

headers = {
    'Host': 'www.tianyancha.com',
    'Referer': 'https://www.tianyancha.com/companies',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

res = requests.get(url, headers=headers)
print(res.text)