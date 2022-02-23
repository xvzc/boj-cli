# boj-cli

백준 온라인 저지 cli 제출

# Chrome extension 설치
`Chrome web store` 에서 **EditThisCookie**를 설치합니다.


# Bash 함수 추가 >> .zshrc
```
function bojlogin() {
    mkdir -p $HOME/.boj-cli
    touch $HOME/boj-handle
    touch $HOME/boj-token
    echo "백준 아이디" > $HOME/.boj-cli/boj-handle
    echo "$1" > $HOME/.boj-cli/boj-token
}
```

`$ source ~/.zshrc`

# BOJ 로그인
 - BOJ 홈페이지에서 자동로그인을 활성화 한후 로그인합니다.
 - EditThisCookie 확장 프로그램을 열어 bojautologin 값의 value를 복사합니다.
 - 쉘에서 `$ bojlogin ${토큰 값}` 을 실행합니다.
 - 토큰 값은 `$HOME/.boj-cli/` 경로에 저장됩니다.

# CLI로 제출하기
`$ python3 boj-submit.py ${소스 파일 절대경로}`를 실행합니다.
