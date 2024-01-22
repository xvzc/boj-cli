import os.path

import pytest

from boj.core.error import IllegalStatementError
from boj.data.boj_info import BojInfo


def test_read(request):
    rootdir = request.config.rootdir
    info = BojInfo.read(
        dir_=os.path.join(rootdir, "tests", "assets", "problems", "3052")
    )
    assert info.id == 3052


def test_find_any_with_backtrace(request):
    rootdir = request.config.rootdir
    info = BojInfo.find_any(
        ongoing_dir="",
        problem_id="",
        cwd=os.path.join(rootdir, "tests", "assets", "problems", "3052"),
    )
    assert info.id == 3052


def test_find_any_with_read(request):
    rootdir = request.config.rootdir
    info = BojInfo.find_any(
        ongoing_dir=os.path.join(rootdir, "tests", "assets", "problems"),
        problem_id="3052",
    )
    assert info.id == 3052


def test_find_upward(request):
    rootdir = request.config.rootdir
    info = BojInfo.find_upward(
        cwd=os.path.join(rootdir, "tests", "assets", "problems", "3052"),
    )
    assert info.id == 3052


@pytest.mark.parametrize(
    "ongoing_dir, problem_id, error",
    [
        (os.path.join(os.getcwd(), "INVALID_DIR"), "", IllegalStatementError),
        (os.path.join(os.getcwd(), "INVALID_DIR"), "1234", IllegalStatementError),
    ],
)
def test_find_any_throw_error(ongoing_dir, problem_id, error):
    with pytest.raises(IllegalStatementError) as e:
        BojInfo.find_any(
            ongoing_dir=ongoing_dir,
            problem_id=problem_id,
        )

    assert e.type == error
