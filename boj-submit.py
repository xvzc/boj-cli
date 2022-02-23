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

home = os.environ.get('HOME')

boj_autologin = ''
with open(home + '/.boj-cli/boj-token', 'r') as file:
    boj_autologin = file.read().strip()


boj_handle = ''
with open(home + '/.boj-cli/boj-handle', 'r') as file:
    boj_handle = file.read().strip()

code = ''
with open(file_path, 'r') as file:
    code = file.read()

url = 'https://www.acmicpc.net/submit/' + problem.id

headers_dict = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
}

response = requests.get('https://www.acmicpc.net', headers=headers_dict)

cookies_dict = {
    'bojautologin': boj_autologin,
    'OnlineJudge': response.cookies.get_dict()['OnlineJudge']
}

response = requests.get(url, headers=headers_dict, cookies=cookies_dict)

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

response = requests.post(url, headers=headers_dict, data=payload, cookies=cookies_dict)

os.system(f'open -a Firefox "https://www.acmicpc.net/status?user_id={boj_handle}"')
