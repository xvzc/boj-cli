import os
import pytest
from boj.core import constant


def test_boj_dir_path():
    assert constant.boj_dir_path() == f'{str(os.getenv("HOME"))}/.boj-cli'


def test_template_dir_path():
    assert constant.template_dir_path() == f'{constant.boj_dir_path()}/templates'


def test_config_file_path():
    assert constant.config_file_path() == f"{constant.boj_dir_path()}/config.yaml"


def test_key_file_path():
    assert constant.key_file_path() == f"{constant.boj_dir_path()}/key"


def test_credential_file_path():
    assert constant.credential_file_path() == f"{constant.boj_dir_path()}/credential"


def test_testcase_file_path():
    assert constant.testcase_file_path() == "./testcase.yaml"


def test_boj_main_url():
    assert constant.boj_main_url() == "https://www.acmicpc.net"


def test_boj_login_url():
    assert constant.boj_login_url() == f"{constant.boj_main_url()}/login?next=%2F"


@pytest.mark.parametrize(
    "problem_id",
    [1234, 1010, 1649, 14500, 1234],
)
def test_boj_submit_url(problem_id):
    assert (
        constant.boj_submit_url(problem_id)
        == f"{constant.boj_main_url()}/submit/{str(problem_id)}"
    )


@pytest.mark.parametrize(
    "problem_id",
    [1234, 1010, 1649, 14500, 1234],
)
def test_boj_problem_url(problem_id):
    assert (
        constant.boj_problem_url(problem_id)
        == f"{constant.boj_main_url()}/problem/{str(problem_id)}"
    )


def test_boj_websocket_url():
    assert (
        constant.boj_websocket_url()
        == "wss://ws-ap1.pusher.com/app/a2cb611847131e062b32?protocol=7&client=js&version=4.2.2&flash=false"
    )


def test_solved_ac_home_url():
    assert constant.solved_ac_home_url() == "https://solved.ac/api/v3"


def test_solved_ac_search_url():
    assert constant.solved_ac_search_url() == f"{constant.solved_ac_home_url()}/search"


def test_solved_ac_search_problem_url():
    assert (
        constant.solved_ac_search_problem_url()
        == f"{constant.solved_ac_search_url()}/problem"
    )
