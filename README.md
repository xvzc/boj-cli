# boj-cli

Command line interface for Baekjoon Online Judge.  

<img src="https://github.com/xvzc/boj-cli/assets/45588457/7e38f42b-be0c-4e56-a4f5-ba5960634a00" width="65%" height="65%">

# Table of contents
<!--ts-->
   * [Installation](#installation)
   * [Configuration](#configuration)
   * [Usage](#usage)
      * [Init](#init)
      * [Login](#login)
      * [Add](#add)
      * [Run](#run)
      * [Submit](#submit)
      * [Clean](#clean)
      * [Open](#open)
      * [Random](#random)
<!--te-->
# Requirements
- `Python <= 3.12`
- `MacOS`, `Linux`, `Windows`

# Installation

```sh
$ pip install boj-cli
```

# Configuration
```yaml
# ~/myproject/.boj/config.yaml
workspace:
  problem_dir: 'src' # Default: "."
  archive_dir: 'archives' # Default: "archives"
filetype:
  py:
    language: 'python3'
    filename: main.py # Defailt: main.{filetype}
    run: 'python3 $file'
  cpp:
    language: 'c++17'
    compile: 'g++ -std=c++17 -O2 -Wall -Wno-sign-compare $file -o a.out'
    run: './a.out'
    after: rm -rf a.out
    manifest_files:
      - compile_flags.txt
  rs:
    language: 'rust2021'
    filename: main.rs # Default: main.{filetype}
    source_dir: src
    compile: 'rustc $file -o main'
    run: './main'
    after: rm -rf ./main
    manifest_files:
      - Cargo.toml
```
> `filetype.language`에 들어갈 수 있는 값들은 [Supported languages](#supported-languages)를 참고해주세요.


# Usage
```
usage: boj [-h] [-v] {init,add,login,open,random,run,submit,clean} ...

positional arguments:
  {init,add,login,open,random,run,submit,clean}
    init                initializes BOJ directory
    add                 sets up an environment of the given problem id
    login               logs in to BOJ
    open                opens a problem of given id in browser
    random              queries and opens a random problem in browser
    run                 runs generated testcases
    submit              submits your solution and trace the realtime statement
    clean               archives accepted source files

options:
  -h, --help            show this help message and exit
  -v, --version         show version
```

## init

```sh
$ boj init
```

현재 경로를 BOJ 디렉토리로 설정하고 다음과 같은 리소스들을 생성합니다.

- `./.boj`
- `./.boj/config.yaml`
- `./.boj/templates`

---

## login

```sh
$ boj login
```

백준 온라인 저지에서는 로그인 시 `reCAPTCHA`를 사용하고있기 때문에 로그인 과정은 조금 번거로울 수 있습니다.
위 명령어를 실행하면 `selenium` 브라우저가 실행되고, `reCAPTCHA`를 포함한 로그인을 수행하면 세션 정보를 로컬 디렉토리 `$HOME/.boj-cli`에 암호화해서 저장합니다.
> 로그인 시 "로그인 상태 유지" 체크 박스를 반드시 선택해주세요.
---

## add

```sh
$ boj add 1234 -f cpp
Testcases have been created.

$ tree .
.
└── 1234
    ├── .boj-info.json
    ├── compile_flags.txt
    ├── main.cpp
    └── testcase.toml
```
백준 온라인 저지 문제를 풀기위한 폴더를 생성하고 다음과 같은 작업들을 수행합니다.
- `./.boj/templates` 폴더에 위치한 템플릿 파일 불러오기.
- 크롤링을 활용해서 toml 파일로 파싱한 테스트케이스 파일 생성.
- manifest 파일 생성. (e.g. package.json, Cargo.toml ...)
- 

```
--filetype, -f str: 파일 타입을 지정합니다. (e.g. cpp, ts, rs, py ...)
```

---

## run
```sh
# Outside of problem dir
$ boj run 1234

# Inside of problem dir
$ cd 1234 && boj run
```
`boj add` 명령어로 생성한 테스트케이스를 활용해 `testcase.toml` 파일에 있는 모든 테스트케이스를 비동기적으로 실행하고
정답을 비교합니다.
> 문제 폴더 안에서 실행하면 문제 번호 인자를 생략할 수 있습니다.
```
--timeout int(sec): 각 테스트케이스의 타임아웃을 설정합니다 (Default: 5초)
```

---

## submit
```sh
# Outside of problem dir
$ boj submit 1234

# Inside of problem dir
$ cd 1234 && boj run
```
로컬 소스 파일을 백준 온라인 저지에 제출하고 채점 현황을 실시간으로 출력합니다.
> 문제 폴더 안에서 실행하면 문제 번호 인자를 생략할 수 있습니다.
```
--open [ open | close | onlyaccepted ]: 코드 공개 여부를 설정합니다.
--timeout int: 제출 현황 웹소켓의 타임아웃 설정(초) (Default: 15)
```

---
## clean
```sh
$ boj clean
```
`boj submit` 명령어 수행 결과로 accepted를 받은 모든 문제들을 `config.workspace.archive_dir`로 아카이브힙니다.  
> 아카이브 되는 파일은 `yyyymmdd_hhmmss_{filename}`의 포멧으로 저장됩니다.
```
--origin, -o: 아카이브 파일 포멧을 무시하고 원본 파일 이름을 사용하며, 파일 이름이 이미 존재하면 덮어씁니다.
```
---

## open
```sh
$ boj open 1234
```
기본 브라우저에서 문제 번호에 해당하는 링크로 이동합니다.

---

## random
```sh
$ boj random --tier g1..g5 --tags dp math
```
solvedac API를 활용해서 문제를 검색하고, 기본 브라우저에서 링크로 이동합니다.
> 여러개의 tags 옵션은 'OR' 조건으로 동작합니다.  
> '내가 풀지 않은 문제' 만 쿼리됩니다.

```
--tier, -i: 문제 티어 쿼리
--tags, -t: 문제 태그 쿼리
```

# Supported languages

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

