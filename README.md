# boj-cli

백준 온라인 저지 cli 제출.  
현재 MacOS에서만 테스트 완료.

# Chrome extension 설치
`Chrome web store` 에서 **EditThisCookie**를 설치합니다.

# Bash 함수 추가 >> .zshrc
- 아래 함수에서 `백준아이디` 라고 적힌 부분을 본인의 BOJ 핸들로 변경한뒤, ~/.zshrc에 추가합니다.

```
function bojlogin() {
    mkdir -p $HOME/.boj-cli
    touch $HOME/boj-handle
    touch $HOME/boj-token
    echo "백준아이디" > $HOME/.boj-cli/boj-handle
    echo "$1" > $HOME/.boj-cli/boj-token
}
```
- 추가된 스크립트를 적용합니다.
`$ source ~/.zshrc`

# BOJ 로그인
 - BOJ 홈페이지에서 자동로그인을 활성화 한후 로그인합니다.
 - EditThisCookie 확장 프로그램을 열어 bojautologin 값의 value를 복사합니다.
 - 쉘에서 `$ bojlogin ${토큰 값}` 을 실행합니다.
 - 토큰 값은 `$HOME/.boj-cli/` 경로에 저장됩니다. 실수로 온라인에 업로드하지 않도록 주의하세요.

> 2022년 2월 기준 한번 로그인을 할 시 토큰은 약 한달간 유효할 것으로 예상됩니다.

# CLI로 제출하기
`$ python3 boj-submit.py ${소스 파일 절대경로}`를 실행합니다.

# 채점 결과 확인하기
 - Firefox 브라우저의 경우 url에 `about:config`를 쳐서 접근하면 고급 옵션을 설정할 수 있습니다.
 - browser.link.open_newwindow 값을 0으로 설정해주세요
 - Firefox 브라우저를 사용하기 싫다면 `boj-submit.py`의 마지막라인에 있는 `open` 커맨드의 어플리케이션 이름을 `Google Chrome` 또는 다른 브라우저로 설정해주세요.
