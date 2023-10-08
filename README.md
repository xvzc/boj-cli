# boj-cli

백준 온라인 저지 커맨드라인 인터페이스  
<img src="https://github.com/xvzc/boj-cli/assets/45588457/f6fcf5b8-b5bd-4674-b018-c6574e98b1c4" width="65%" height="65%">

# 설치
`$ pip install boj-cli`

# 로컬 설정
`filetype.default_language`에 들어갈 수 있는 값들은 [지원 언어](#지원-언어)를 참고해주세요.

> ~/.boj-cli/config.json
```yaml
command:
  init:
    lang: cpp # Make sure that you have ~/.boj-cli/templates/template.cpp
  random:
    tier: g1..g5
    tags:
      - dp
      - math
  run:
    verbose: false
    timeout: 15
  submit:
    verbose: false
    timeout: 15
    open: onlyaccepted
filetype:
  py:
    default_language: 'python3'
    run: 'python3 $file'
  cpp:
    default_language: 'c++17'
    compile: |
      g++ -std=c++17 -O2 -Wall -Wno-sign-compare $file -o a.out
    run: './a.out'

```

# 사용법
```
$ boj --help
usage: boj [-h] [-v] {login,submit,open,run,init,random} ...

positional arguments:
  {login,submit,open,run,init,random}
    login               logs in to BOJ
    submit              submits your solution and trace the realtime statement
    open                opens a problem of given id in browser
    run                 runs generated testcases
    init                creates testcases in current directory
    random              queries and opens a random problem in browser

options:
  -h, --help            show this help message and exit
  -v, --version         show version
```

## 로그인
백준 온라인 저지에서는 로그인 시 `reCAPTCHA`를 사용하고있기 때문에 로그인 과정은 조금 번거로울 수 있습니다. 
```
$ boj login
```

위 명령어를 실행하면 `selenium` 브라우저가 실행됩니다. 로그인 정보를 입력하고 `reCAPTCHA`를 수행하면 로그인 세션 정보는 암호화되어 저장됩니다.
> 로그인 시 "로그인 상태 유지" 체크 박스를 반드시 선택해주세요.

---

## 테스트케이스 및 템플릿 파일 불러오기
백준 온라인저지에 올라와있는 문제에서 테스트케이스를 추려내어 현재 경로에 `testcase.yaml` 파일을 생성합니다.
생성된 `testcase.yaml`의 포멧에 맞게 커스텀 테스트케이스 또한 추가할 수 있습니다.
`lang` 옵션에 값을 할당하면 템플릿 파일을 읽어 현재 경로에 `{문제번호}.{언어}` 파일을 생성합니다.
```
$ boj init {PROBLEM_ID}
```

### Options
```
--lang str: 언어를 특정해서 ~/.boj-cli/templates/template.{lang} 파일을 읽어올 수 있도록 합니다.
            값이 존재하지 않으면 템플릿 파일을 불러오지 않습니다.
```

---

## 테스트케이스 실행하기
`init` 명령어로 생성한 테스트케이스를 활용해 `testcase.yaml` 파일에 있는 모든 테스트케이스를 비동기적으로 실행하고
정답을 비교합니다.
```
$ boj run {FILE_PATH}
```

### Options
```
--verbose bool: 자세한 아웃풋을 출력합니다. (예: 컴파일 에러)  
--timeout int(sec): 각 테스트케이스의 타임아웃을 설정합니다 (Default: 5초)
```

---

## 코드 제출하기
로컬 소스 파일을 백준 온라인 저지에 제출하고 채점 현황을 실시간으로 출력합니다.
```
$ boj submit {FILE_PATH}
ex) boj submit ./1234.cpp
```

### Options
```
--lang str: 제출할 언어를 선택합니다. 옵션이 주어지지 않은경우 local config 값으로 실행됩니다.
--open [ open | close | onlyaccepted ]: 코드 공개 여부를 설정합니다.
```

---

## 브라우저에서 문제 링크 열기
문제 링크를 기본 브라우저에서 엽니다.
```
$ boj open {PROBLEM_ID}
ex) boj open 1234
```

---

## 랜덤 문제 브라우저에서 열기
랜덤 문제 링크를 기본 브라우저에서 엽니다.
```
$ boj random --tier g1..g5 --tags dp math
```

> 여러개의 tags 옵션은 OR 조건으로 동작합니다.
> '내가 풀지 않은 문제' 만 쿼리됩니다.

### Options
```
--tier: 문제 티어 쿼리
--tags: 문제 태그 쿼리
```

# 지원 언어
- `c++17`
- `python3`
- `pypy3`
- `c11`
- `text`
- `golfscript`
- `java8`
- `c++98`
- `ruby`
- `c99`
- `c++11`
- `java11`
- `kotlin(jvm)`
- `c++14`
- `swift`
- `java8(openjdk)`
- `c++20`
- `c#`
- `node.js`
- `go`
- `d`
- `rust2018`
- `go(gccgo)`
- `c++17(clang)`
- `java15`
- `d(ldc)`
- `php`
- `rust2015`
- `pascal`
- `lua`
- `perl`
- `f#`
- `visual-basic`
- `objective-c`
- `objective-c++`
- `c99(clang)`
- `c++98(clang)`
- `c++11(clang)`
- `c++14(clang)`
- `c11(clang)`
- `c++20(clang)`
- `c90`
- `c2x`
- `c90(clang)`
- `c2x(clang)`
- `typescript`
- `assembly(32bit)`
- `assembly(64bit)`
- `bash`
- `fortran`
- `scheme`
- `ada`
- `awk`
- `o-caml`
- `brainf**k`
- `whitespace`
- `tcl`
- `rhino`
- `cobol`
- `pike`
- `sed`
- `intercal`
- `bc`
- `algol68`
- `befunge`
- `free-basic`
- `haxe`
- `lolcode`
- `아희`
- `system-verilog`
- `rust2021`
- `scala`

