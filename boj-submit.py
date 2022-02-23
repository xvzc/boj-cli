import requests
from bs4 import BeautifulSoup
import os
import sys
import ntpath


class Problem:
    id = 0
    language = ''

    def __init__(self, id, language):
        self.id = id
        self.language = language

    def __repr__(self):
        return 'Problem {' + self.id + ', ' + self.language + '}'


    def of(full_path):
        tokens = ntpath.basename(full_path).split('.')
        id = tokens[0]
        language = tokens[1]
        return Problem(id, language)


languages = {
    'cpp': 84,  # default C++ 17
    'py': 28,
    'c': 75,
    'txt': 58,
    'java': 93,  # default jdk 11
    'kts': 69
}

args = sys.argv
file_path = args[1]
problem = Problem.of(file_path)

boj_cli_path = os.environ.get('BAEKJOON_CLI')

boj_autologin = ''
with open(boj_cli_path + '/boj-token', 'r') as file:
    boj_autologin = file.read().strip()


boj_handle = ''
with open(boj_cli_path + '/boj-handle', 'r') as file:
    boj_handle = file.read().strip()

code = ''
with open(file_path, 'r') as file:
    code = file.read()

url = 'https://www.acmicpc.net/submit/' + problem.id

headers_dict = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.acmicpc.net/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'Cookie': 'gads=ID=bfe15dbf021ab9b5-22fb37c0a5d0008f:T=1645096265:RT=1645096265:S=ALNI_MbEUfMusoZkcXo3fh-J-kSkeCiwPg; _fbp=fb.1.1645095982499.1868301201; _ga=GA1.1.1519934818.1645095984;'
}

response = requests.get('https://www.acmicpc.net', headers=headers_dict)

cookies_dict = {
    'bojautologin': boj_autologin,
    'OnlineJudge': response.cookies.get_dict()['OnlineJudge']
}

response = requests.get(url, headers=headers_dict, cookies=cookies_dict)
print(response.cookies.get_dict())

html = response.text
soup = BeautifulSoup(html, 'html.parser')
input_tags = soup.select('input')

if input_tags[1]['name'] == 'login_user_id':
    print('Login required')
    exit(0)

csrf_key = ""
for i in input_tags:
    if i['name'] == 'csrf_key':
        csrf_key = i['value']

payload = {
    'problem_id': problem.id,
    'language': languages[problem.language],
    'code_open': 'open',
    'source': code,
    'csrf_key': csrf_key
}

response = requests.post(url, data=payload, cookies=cookies_dict)

os.system(f'open -a Firefox "https://www.acmicpc.net/status?user_id={boj_handle}"')
