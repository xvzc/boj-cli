import os


def boj_dir_path():
    return f'{str(os.getenv("HOME"))}/.boj-cli'


def config_file_path():
    return f"{boj_dir_path()}/config.yaml"


def key_file_path():
    return f"{boj_dir_path()}/key"


def template_dir_path():
    return f"{boj_dir_path()}/templates"


def credential_file_path():
    return f"{boj_dir_path()}/credential"


def testcase_file_path():
    return f"./testcase.yaml"


def boj_main_url():
    return "https://www.acmicpc.net"


def boj_login_url():
    return f"{boj_main_url()}/login?next=%2F"


def boj_submit_url(problem_id):
    return f"{boj_main_url()}/submit/{str(problem_id)}"


def boj_problem_url(problem_id):
    return f"{boj_main_url()}/problem/{str(problem_id)}"


def boj_websocket_url():
    return "wss://ws-ap1.pusher.com/app/a2cb611847131e062b32?protocol=7&client=js&version=4.2.2&flash=false"


def solved_ac_home_url():
    return "https://solved.ac/api/v3"


def solved_ac_search_url():
    return f"{solved_ac_home_url()}/search"


def solved_ac_search_problem_url():
    return f"{solved_ac_search_url()}/problem"


def default_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/98.0.4758.102 Safari/537.36 "
    }


def lang_dict():
    return {
        "c++17": 84,
        "python3": 28,
        "pypy3": 73,
        "c11": 75,
        "text": 58,
        "golfscript": 79,
        "java8": 3,
        "c++98": 1,
        "ruby": 68,
        "c99": 0,
        "c++11": 49,
        "java11": 93,
        "kotlin(jvm)": 69,
        "c++14": 88,
        "swift": 74,
        "java8(openjdk)": 91,
        "c++20": 95,
        "c#": 86,
        "node.js": 17,
        "go": 12,
        "d": 29,
        "rust2018": 94,
        "go(gccgo)": 90,
        "c++17(clang)": 85,
        "java15": 107,
        "d(ldc)": 100,
        "php": 7,
        "rust2015": 44,
        "pascal": 2,
        "lua": 16,
        "perl": 8,
        "f#": 108,
        "visual-basic": 109,
        "objective-c": 10,
        "objective-c++": 64,
        "c99(clang)": 59,
        "c++98(clang)": 60,
        "c++11(clang)": 66,
        "c++14(clang)": 67,
        "c11(clang)": 77,
        "c++20(clang)": 96,
        "c90": 101,
        "c2x": 102,
        "c90(clang)": 103,
        "c2x(clang)": 104,
        "typescript": 106,
        "assembly(32bit)": 27,
        "assembly(64bit)": 87,
        "bash": 5,
        "fortran": 13,
        "scheme": 14,
        "ada": 19,
        "awk": 21,
        "o-caml": 22,
        "brainf**k": 23,
        "whitespace": 24,
        "tcl": 26,
        "rhino": 34,
        "cobol": 35,
        "pike": 41,
        "sed": 43,
        "intercal": 47,
        "bc": 48,
        "algol68": 70,
        "befunge": 71,
        "free-basic": 78,
        "haxe": 81,
        "lolcode": 82,
        "아희": 83,
        "system-verilog": 105,
        "rust2021": 113,
        "scala": 15,
    }
