# boj-cli

백준 온라인 저지 cli 제출.  
현재 MacOS에서만 테스트 완료.

# Chrome extension 설치
`Chrome web store` 에서 **EditThisCookie**를 설치ㄱㄱ.

# Bash 함수 추가 >> .zshrc
- 아래 함수에서 `백준아이디` 라고 적힌 부분을 본인의 BOJ 핸들로 변경하고, ~/.zshrc에 추가

```
function bojlogin() {
    mkdir -p $HOME/.boj-cli
    touch $HOME/boj-handle
    touch $HOME/boj-token
    echo "백준아이디" > $HOME/.boj-cli/boj-handle
    echo "$1" > $HOME/.boj-cli/boj-token
}
```
- 추가된 스크립트를 적용.
`$ source ~/.zshrc`

# 자동 제출 스크립트 설치
`$ curl -fsSL https://raw.githubusercontent.com/xvzc/boj-cli/main/install.sh | bash`
스크립트는 ~/.boj-cli에 설치됨

# BOJ 로그인
 - BOJ 홈페이지에서 자동로그인을 활성화 한후 로그인.
 - EditThisCookie 확장 프로그램을 열어 bojautologin 값의 value를 복사.
 - 쉘에서 `$ bojlogin ${토큰 값}` 을 실행.
 - 토큰 값은 `$HOME/.boj-cli/` 경로에 저장됨. 
 > 토큰 값은 실수로 github 같은 곳에 올리지 마세욤

> 2022년 2월 기준 한번 로그인을 할 시 토큰은 약 한달간 유효할 것으로 예상됨.

# CLI로 제출하기
`$ python3 boj-submit.py ${소스 파일 절대경로}`를 실행합니다.
> 소스 파일명은 `문제번호.언어` 형식으로 해주세여 왜냐면 소스 파일 절대경로를 파싱해서 문제번호를 얻어내기때문에 .... 

# 채점 결과 확인할 때 팁
boj-summit.py 마지막 줄이 브라우저를 실행해서 채점 결과 확인하는 부분인데, Firefox 브라우저 사용하면 매 제출 마다 새로운 탭이 아닌 현재탭에서 띄우도록 설정할 수 있음.

 - Firefox 브라우저의 경우 url에 `about:config`를 입력해서 고급 옵션ㄱㄱ .
 - browser.link.open_newwindow 값을 0으로 바꿈
 - Firefox 브라우저를 사용하기 싫으면 `boj-submit.py`의 마지막라인에 있는 `open` 커맨드의 어플리케이션 이름을 `Google Chrome` 또는 다른 브라우저로 설정하샘. 대신 제출 할 때 마다 새로운 탭 뜸.
