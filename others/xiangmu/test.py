import requests
url='http://www.zaofang.net/yushou/list.php?type=1&page=5'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}
response=requests.get('http://www.jyfdc.com/House/CaseProjectInfo?CaseId=010605290020')
print(response.status_code)